#ifndef GRAPHDOT_MARGINALIZED_KERNEL_H_
#define GRAPHDOT_MARGINALIZED_KERNEL_H_

#include <algorithm>
#include "util_cuda.h"
#include "graph.h"
#include "fmath.h"
#include "array.h"

namespace graphdot {

namespace marginalized {

struct job_t {
    int i, j;
    float * __restrict vr;
};

struct pcg_scratch_t {

    float * __restrict ptr;
    int stride;

    pcg_scratch_t(pcg_scratch_t const & other) = default;
 
    __device__ __inline__ float * x() { return ptr + stride * 0; }
    __device__ __inline__ float * r() { return ptr + stride * 1; }
    __device__ __inline__ float * z() { return ptr + stride * 2; }
    __device__ __inline__ float * p() { return ptr + stride * 3; }
    __device__ __inline__ float * Ap() { return ptr + stride * 4; }
    __device__ __inline__ float & x(int i) { return x()[i]; }
    __device__ __inline__ float & r(int i) { return r()[i]; }
    __device__ __inline__ float & z(int i) { return z()[i]; }
    __device__ __inline__ float & p(int i) { return p()[i]; }
    __device__ __inline__ float & Ap(int i) { return Ap()[i]; }
};

/*-----------------------------------------------------------------------------
CG solver based on on-the-fly Kronecker product matrix-vector (XMV) operations
-----------------------------------------------------------------------------*/
template<class Graph> struct labeled_compact_block_dynsched_pcg {
    /*  Each octile contains up to 64 elemented in column-major format
        =========================================
        |  0 |  8 | 16 | 24 | 32 | 40 | 48 | 56 |
        -----------------------------------------
        |  1 |  9 | 17 | 25 | 33 | 41 | 49 | 57 |
        -----------------------------------------
        |  2 | 10 | 18 | 26 | 34 | 42 | 50 | 58 |
        -----------------------------------------
        |  3 | 11 | 19 | 27 | 35 | 43 | 51 | 59 |
        -----------------------------------------
        |  4 | 12 | 20 | 28 | 36 | 44 | 52 | 60 |
        -----------------------------------------
        |  5 | 13 | 21 | 29 | 37 | 45 | 53 | 61 |
        -----------------------------------------
        |  6 | 14 | 22 | 30 | 38 | 46 | 54 | 62 |
        -----------------------------------------
        |  7 | 15 | 23 | 31 | 39 | 47 | 55 | 63 |
        =========================================
        The right-hand side is a 64-element vector */

    using graph_t   = Graph;
    using scratch_t = pcg_scratch_t;
    using node_t    = typename graph_t::node_t;
    using edge_t    = typename graph_t::edge_t;

    constexpr static int octile_w = 8;
    constexpr static int octile_h = 8;

    // maps a piece of shared memory as an octile for matvec computation
    struct octile {

        edge_t * const _data;

        constexpr static int size_bytes = octile_w * octile_h * sizeof(edge_t);

        __device__ __inline__ octile(void * ptr)
            : _data(reinterpret_cast<edge_t *>(ptr)) {}

        __device__ __inline__ edge_t & operator()(int i, int j) {
            return _data[i + j * octile_h];
        }

        __device__ __inline__ edge_t & operator()(int i) { return _data[i]; }
    };

    // maps a piece of shared memory as 4 hexdectors for matvec computation
    struct rhs {

        float * const _data;

        constexpr static int size_bytes = octile_w * octile_w * sizeof(float);

        __device__ __inline__ rhs(void * ptr)
            : _data(reinterpret_cast<float *>(ptr)) {}

        __device__ __inline__ float & operator()(int j1, int j2) {
            return _data[j1 * octile_w + j2];
        }
    };

    struct rhsduo {

        float2 * const _data;

        constexpr static int size_bytes = octile_w * octile_w * sizeof(float2);

        __device__ __inline__ rhsduo(void * ptr)
            : _data(reinterpret_cast<float2 *>(ptr)) {}

        __device__ __inline__ float2 & operator()(int j1, int j2) {
            return _data[j1 * octile_w + j2];
        }
    };

    struct nzlist {
        using nzindex_t = int;

        nzindex_t * _data;

        constexpr static int size_bytes =
            octile_w * octile_h * sizeof(nzindex_t);

        __device__ __inline__ nzlist(void * ptr)
            : _data(reinterpret_cast<nzindex_t *>(ptr)) {}

        __device__ __inline__ nzindex_t & operator()(int i) { return _data[i]; }

        __device__ __inline__ nzindex_t const & operator()(int i) const {
            return _data[i];
        }
    };

    constexpr static int shmem_bytes_per_warp =
        2 * octile::size_bytes +
        2 * nzlist::size_bytes +
        // the staging buffer can share space with rhs due to temporal mutual exclusion
        std::max(std::max(octile::size_bytes, rhs::size_bytes), rhsduo::size_bytes);

    // Expand a submatrix in compact format in shared memory
    template<class CompactTile>
    __device__ __inline__ static void load(const int lane, CompactTile const ctile, octile oct, nzlist nzl, octile swap) {
        
        using namespace graphdot::cuda;
        
        const int nnz1 = __popcll(ctile.nzmask);
        if (lane             < nnz1) swap(lane)             = ctile.elements[lane];
        if (lane + warp_size < nnz1) swap(lane + warp_size) = ctile.elements[lane + warp_size];

        __syncwarp();

        if (ctile.nzmask_halves[0] & (1 << lane)) {
            int src = __popc(ctile.nzmask_halves[0] & lanemask_lt());
            oct(lane) = swap(src);
            nzl(src)  = lane;
        }

        if (ctile.nzmask_halves[1] & (1 << lane)) {
            int src = __popc(ctile.nzmask_halves[1] & lanemask_lt()) +
                      __popc(ctile.nzmask_halves[0]);
            oct(lane + warp_size) = swap(src);
            nzl(src)              = lane + warp_size;
        }
    }

    template<class NodeKernel, class EdgeKernel>
    __inline__ __device__ static void compute(
        NodeKernel const node_kernel,
        EdgeKernel const edge_kernel,
        Graph const    g1,
        Graph const    g2,
        scratch_t      scratch,
        char * const   cache,
        const float    q,
        const float    q0) {

        using namespace graphdot::cuda;

        const int warp_id_local  = threadIdx.x / warp_size;
        const int warp_num_local = blockDim.x / warp_size;
        const int lane           = laneid();
        const int n1             = g1.n_node;
        const int n2             = g2.n_node;
        const int N              = n1 * n2;
        const int i1_upper       =  lane              / octile_h;
        const int i1_lower       = (lane + warp_size) / octile_h;
        const int i2             =  lane              % octile_h;

        octile octilex {cache
                        + warp_id_local * shmem_bytes_per_warp
                        + octile::size_bytes * 2
                        + nzlist::size_bytes * 2};

        for (int i = threadIdx.x; i < N; i += blockDim.x) {
            const int   i1 = i / n2;
            const int   i2 = i % n2;
            const float d1 = g1.degree[i1];
            const float d2 = g2.degree[i2];
            const float dx = d1 * d2 / ipow<2>(1 - q);
            const float vx = node_kernel(g1.node[i1], g2.node[i2]);

            // b  = Dx . qx
            const auto b = dx * q * q / (q0 * q0);
            // r0 = b - A . x0
            //    = b
            const auto r0 = b; 
            // z0 = M^-1 . r0
            //    = (Dx . Vx^-1)^-1 . r0
            //    = r0 .* Vx ./ Dx
            const auto z0 = r0 * vx / dx;
            const auto p0 = z0;

            scratch.x(i) = 0;  // x0 === 0
            scratch.r(i) = r0;
            scratch.z(i) = z0;
            scratch.p(i) = p0;

            // Ap = diag(A . p0)
            //    = Dx . Vx^-1 . p0
            scratch.Ap(i) = dx / vx * p0;
        }
        __syncthreads();

        auto rTz = block_vdotv(scratch.r(), scratch.z(), N);

        int k;
        for (k = 0; k < N; ++k) {

            // Ap = A * p, off-diagonal part
            for (int O1 = 0; O1 < g1.n_octile; O1 += warp_num_local) {

                const int nt1 = min(g1.n_octile - O1, warp_num_local);

                if (warp_id_local < nt1) {
                    // load the first submatrix in compact format into shared memory
                    octile octile1 {cache + warp_id_local * shmem_bytes_per_warp};
                    nzlist nzlist1 {cache + warp_id_local * shmem_bytes_per_warp + octile::size_bytes};
                    load(lane, g1.octile[O1 + warp_id_local], octile1, nzlist1, octilex);
                }

                __syncthreads();

                for (int O2 = 0; O2 < g2.n_octile; O2 += warp_num_local) {

                    const int nt2 = min(g2.n_octile - O2, warp_num_local);

                    if (warp_id_local < nt2) {
                        // load the second submatrix in compact fornat into shared memory
                        octile octile2 {cache + warp_id_local * shmem_bytes_per_warp + octile::size_bytes + nzlist::size_bytes};
                        nzlist nzlist2 {cache + warp_id_local * shmem_bytes_per_warp + octile::size_bytes + nzlist::size_bytes + octile::size_bytes};
                        load(lane, g2.octile[O2 + warp_id_local], octile2, nzlist2, octilex);
                    }

                    __syncthreads();

                    for (int t = warp_id_local; t < nt1 * nt2; t += warp_num_local) {

                        const int p1 = t / nt2;
                        const int p2 = t % nt2;

                        const auto o1  = g1.octile[O1 + p1];
                        const auto o2  = g2.octile[O2 + p2];
                        const int nnz1 = __popcll(o1.nzmask);
                        const int nnz2 = __popcll(o2.nzmask);
                        const int I1   = o1.upper;
                        const int J1   = o1.left;
                        const int I2   = o2.upper;
                        const int J2   = o2.left;

                        octile octile1 {cache + p1 * shmem_bytes_per_warp};
                        octile octile2 {cache + p2 * shmem_bytes_per_warp + octile::size_bytes + nzlist::size_bytes};
                        rhs    rhs     {cache + warp_id_local * shmem_bytes_per_warp + octile::size_bytes * 2 + nzlist::size_bytes * 2};

                        // load RHS
                        int j1 = lane / octile_w;
                        int j2 = lane % octile_w;
                        if (J1 + j1                        < n1 && J2 + j2 < n2) rhs (j1,                        j2) = scratch.p((J1 + j1                       ) * n2 + (J2 + j2));
                        if (J1 + j1 + warp_size / octile_w < n1 && J2 + j2 < n2) rhs (j1 + warp_size / octile_w, j2) = scratch.p((J1 + j1 + warp_size / octile_w) * n2 + (J2 + j2));

                        if (nnz1 * nnz2 >= 256) {
                            // dense x dense
                            float sum_upper = 0, sum_lower = 0;

                            #if 1
                            for (int j1 = 0, colmask1 = 1; j1 < octile_w && j1 < g1.n_node - J1; ++j1, colmask1 <<= 1) {
                                auto e1_upper = octile1(i1_upper, j1);
                                auto e1_lower = octile1(i1_lower, j1);
                                bool m1_upper = o1.nzmask_r_bytes[i1_upper] & colmask1;
                                bool m1_lower = o1.nzmask_r_bytes[i1_lower] & colmask1;
                    
                                #pragma unroll (octile_w)
                                for (int j2 = 0, colmask2 = 1; j2 < octile_w; ++j2, colmask2 <<= 1) {
                                    if (o2.nzmask_r_bytes[i2] & colmask2) {
                                        auto e2 = octile2(i2, j2);
                                        auto r  = rhs(j1, j2);
                                        sum_upper -= r * (m1_upper ? edge_kernel(e1_upper, e2) : 0.f);
                                        sum_lower -= r * (m1_lower ? edge_kernel(e1_lower, e2) : 0.f);
                                    }
                                }
                            }
                            #else
                            for (int j1 = 0; j1 < octile_w && j1 < g1.n_node - J1; ++j1) {
                                auto e1_upper = octile1 (i1_upper, j1);
                                auto e1_lower = octile1 (i1_lower, j1);
                                auto m1_upper = 1ULL << (i1_upper + j1 * octile_h);
                                auto m1_lower = 1ULL << (i1_lower + j1 * octile_h);
                    
                                #pragma unroll (octile_w)
                                for (int j2 = 0, mask = 1; j2 < octile_w; ++j2, mask <<= 1) {
                                    auto e2 = octile2 (i2, j2);
                                    auto r  = rhs (j1, j2);
                                    auto m2 = 1ULL << (i2 + j2 * octile_h);
                                    if ((o1.nzmask & m1_upper) && (o2.nzmask & m2)) {
                                        sum_upper -= edge_kernel(e1_upper, e2) * r;
                                    }
                                    if ((o1.nzmask & m1_lower) && (o2.nzmask & m2)) {
                                        sum_lower -= edge_kernel(e1_lower, e2) * r ;
                                    }
                                }
                            }
                            #endif

                            atomicAdd(&scratch.Ap((I1 + i1_upper) * n2 + (I2 + i2)), sum_upper);
                            atomicAdd(&scratch.Ap((I1 + i1_lower) * n2 + (I2 + i2)), sum_lower);

                        } else {
                            // sparse x sparse
                            nzlist nzlist1 {cache + p1 * shmem_bytes_per_warp + octile::size_bytes};
                            nzlist nzlist2 {cache + p2 * shmem_bytes_per_warp + octile::size_bytes + nzlist::size_bytes + octile::size_bytes};

                            for (int i = lane; i < nnz1 * nnz2; i += warp_size) {
                                int  k1 = i / nnz2;
                                int  k2 = i - k1 * nnz2;
                                int  p1 = nzlist1(k1);
                                int  p2 = nzlist2(k2);
                                int  i1 = p1 % octile_h;
                                int  j1 = p1 / octile_h;
                                int  i2 = p2 % octile_h;
                                int  j2 = p2 / octile_h;
                                auto e1 = octile1(p1);
                                auto e2 = octile2(p2);
                                auto r  = rhs(j1, j2);
                                atomicAdd(&scratch.Ap((I1 + i1) * n2 + (I2 + i2)), -edge_kernel(e1, e2) * r);
                            }
                        }
                    }

                    __syncthreads();
                }
            }

            __syncthreads();

            // alpha = rTr / dot( p, Ap );
            auto pAp   = block_vdotv(scratch.p(), scratch.Ap(), N);
            auto alpha = rTz / pAp;

            // x = x + alpha * p;
            // r = r - alpha * Ap;
            // z = M^-1 . r
            //   = (Dx . Vx^-1)^-1 . r
            //   = Vx . r ./ Dx
            // rTr      = r^T . r
            // rTz_next = r^T . z
            float rTr = 0, rTz_next = 0;
            for (int i = threadIdx.x; i < N; i += blockDim.x) {
                const int i1 = i / n2;
                const int i2 = i % n2;
                const float d1 = g1.degree[i1] / (1 - q);
                const float d2 = g2.degree[i2] / (1 - q);
                const float dx = d1 * d2;
                const float vx = node_kernel(g1.node[i1], g2.node[i2]);


                scratch.x(i) += alpha * scratch.p(i);
                scratch.r(i) -= alpha * scratch.Ap(i);
                scratch.z(i)  = vx / dx * scratch.r(i);
                rTr      += scratch.r(i) * scratch.r(i);
                rTz_next += scratch.r(i) * scratch.z(i);
            }

            // rTr      = block_sum(rTr);
            // rTz_next = block_sum(rTz_next);
            __shared__ float sum1, sum2;
            if (threadIdx.x == 0) sum1 = 0, sum2 = 0;
            #pragma unroll
            for (int p = (warp_size >> 1); p >= 1; p >>= 1) {
                rTr      += __shfl_xor_sync(0xFFFFFFFF, rTr, p);
                rTz_next += __shfl_xor_sync(0xFFFFFFFF, rTz_next, p);
            }
            __syncthreads();
            if (laneid() == 0) {
                atomicAdd(&sum1, rTr);
                atomicAdd(&sum2, rTz_next);
            }
            __syncthreads();
            rTr      = sum1;
            rTz_next = sum2;

            if (sqrtf(rTr) < 1e-10f * N) break;

            // beta = rTz_next / rTz;
            auto beta = rTz_next / rTz;

            // p = r + beta * p;
            for (int i = threadIdx.x; i < N; i += blockDim.x) {
                const int i1 = i / n2;
                const int i2 = i % n2;
                const float p  = scratch.z(i) + beta * scratch.p(i);
                scratch.p(i)   = p;

                const float d1 = g1.degree[i1] / (1 - q);
                const float d2 = g2.degree[i2] / (1 - q);
                const float dx = d1 * d2;
                const float vx = node_kernel(g1.node[i1], g2.node[i2]);
                scratch.Ap(i)  = dx / vx * p;
            }
            __syncthreads();

            rTz = rTz_next;
        }

        #if 0
        __syncthreads();
        float R = 0;
        for (int i = threadIdx.x; i < N; i += blockDim.x) {
            R += scratch.x (i);
        }
        R = warp_sum (R);
        __shared__ float block_R;
        if (threadIdx.x == 0) block_R = 0;
        __syncthreads();
        if (laneid() == 0) atomicAdd (&block_R, R);
        __syncthreads();
        if (threadIdx.x == 0) {
            printf ("sum(R) = %.7f\n", block_R);
            printf ("Converged after %d iterations\n", k);
            #if 0
            for (int ij = 0; ij < N; ++ij) {
                printf ("solution x[%d] = %.7f\n", ij, scratch.x (ij));
            }
            #endif
        }
        __syncthreads();
        #endif
    }

    template<class NodeKernel, class EdgeKernel, class StartingProbability>
    __inline__ __device__ static void compute_duo(
        NodeKernel const node_kernel,
        EdgeKernel const edge_kernel,
        StartingProbability const p_start,
        Graph const    g1,
        Graph const    g2,
        scratch_t      scratch,
        char * const   cache,
        const float    q,
        const float    q0) {

        using namespace graphdot::cuda;

        const int warp_id_local  = threadIdx.x / warp_size;
        const int warp_num_local = blockDim.x / warp_size;
        const int lane           = laneid();
        const int n1             = g1.n_node;
        const int n2             = g2.n_node;
        const int N              = n1 * n2;
        const int i1_upper       =  lane              / octile_h;
        const int i1_lower       = (lane + warp_size) / octile_h;
        const int i2             =  lane              % octile_h;

        octile octilex {cache
                        + warp_id_local * shmem_bytes_per_warp
                        + octile::size_bytes * 2
                        + nzlist::size_bytes * 2};

        for (int i = threadIdx.x; i < N; i += blockDim.x) {
            const int   i1 = i / n2;
            const int   i2 = i % n2;
            const float d1 = g1.degree[i1];
            const float d2 = g2.degree[i2];
            const float dx = d1 * d2 / ipow<2>(1 - q);
            const float vx = node_kernel(g1.node[i1], g2.node[i2]);

            // b  = Dx . qx
            const auto b = dx * q * q / (q0 * q0);
            // r0 = b - A . x0
            //    = b
            const auto r0 = b; 
            // z0 = M^-1 . r0
            //    = (Dx . Vx^-1)^-1 . r0
            //    = r0 .* Vx ./ Dx
            const auto z0 = r0 * vx / dx;
            const auto p0 = z0;

            scratch.x(i) = 0;  // x0 === 0
            scratch.r(i) = r0;
            scratch.z(i) = z0;
            scratch.p(i) = p0;
            
            const auto bX = p_start(g1.node[i1]) * p_start(g2.node[i2]);
            const auto rX = bX;
            const auto zX = rX * vx / dx;
            const auto pX = zX;

            scratch.x(i + N) = 0;
            scratch.r(i + N) = rX;
            scratch.z(i + N) = zX;
            scratch.p(i + N) = pX;
        }
        __syncthreads();

        auto rTz = block_vdotv(scratch.r(), scratch.z(), 2 * N);

        int k;
        for (k = 0; k < N; ++k) {
            // Ap = A * p, diagonal part
            // diag(A . p0) = Dx . Vx^-1 . p0
            for (int i = threadIdx.x; i < N; i += blockDim.x) {
                const int i1 = i / n2;
                const int i2 = i % n2;
                const float d1 = g1.degree[i1];
                const float d2 = g2.degree[i2];
                const float dx = d1 * d2 / ipow<2>(1 - q);
                const float vx = node_kernel(g1.node[i1], g2.node[i2]);
            
                #pragma unroll 2
                for(int k = 0; k < 2; ++k) {
                    scratch.Ap(i + k * N)  = dx / vx * scratch.p(i + k * N);
                }
            }
            __syncthreads();

            // Ap = A * p, off-diagonal part
            for (int O1 = 0; O1 < g1.n_octile; O1 += warp_num_local) {

                const int nt1 = min(g1.n_octile - O1, warp_num_local);

                if (warp_id_local < nt1) {
                    // load the first submatrix in compact format into shared memory
                    octile octile1 {cache + warp_id_local * shmem_bytes_per_warp};
                    nzlist nzlist1 {cache + warp_id_local * shmem_bytes_per_warp + octile::size_bytes};
                    load(lane, g1.octile[O1 + warp_id_local], octile1, nzlist1, octilex);
                }

                __syncthreads();

                for (int O2 = 0; O2 < g2.n_octile; O2 += warp_num_local) {

                    const int nt2 = min(g2.n_octile - O2, warp_num_local);

                    if (warp_id_local < nt2) {
                        // load the second submatrix in compact fornat into shared memory
                        octile octile2 {cache + warp_id_local * shmem_bytes_per_warp + octile::size_bytes + nzlist::size_bytes};
                        nzlist nzlist2 {cache + warp_id_local * shmem_bytes_per_warp + octile::size_bytes + nzlist::size_bytes + octile::size_bytes};
                        load(lane, g2.octile[O2 + warp_id_local], octile2, nzlist2, octilex);
                    }

                    __syncthreads();

                    for (int t = warp_id_local; t < nt1 * nt2; t += warp_num_local) {

                        const int p1 = t / nt2;
                        const int p2 = t % nt2;

                        const auto o1  = g1.octile[O1 + p1];
                        const auto o2  = g2.octile[O2 + p2];
                        const int nnz1 = __popcll(o1.nzmask);
                        const int nnz2 = __popcll(o2.nzmask);
                        const int I1   = o1.upper;
                        const int J1   = o1.left;
                        const int I2   = o2.upper;
                        const int J2   = o2.left;

                        octile octile1 {cache + p1 * shmem_bytes_per_warp};
                        octile octile2 {cache + p2 * shmem_bytes_per_warp + octile::size_bytes + nzlist::size_bytes};
                        rhsduo rhs     {cache + warp_id_local * shmem_bytes_per_warp + octile::size_bytes * 2 + nzlist::size_bytes * 2};

                        // load RHS
                        int j1 = lane / octile_w;
                        int j2 = lane % octile_w;
                        if (J1 + j1                        < n1 && J2 + j2 < n2) {
                            rhs (j1,                        j2) = make_float2(
                                scratch.p((J1 + j1                       ) * n2 + (J2 + j2)),
                                scratch.p((J1 + j1                       ) * n2 + (J2 + j2) + N)
                            );
                        }
                        if (J1 + j1 + warp_size / octile_w < n1 && J2 + j2 < n2) {
                            rhs (j1 + warp_size / octile_w, j2) = make_float2(
                                scratch.p((J1 + j1 + warp_size / octile_w) * n2 + (J2 + j2)),
                                scratch.p((J1 + j1 + warp_size / octile_w) * n2 + (J2 + j2) + N)
                            );
                        }

                        if (nnz1 * nnz2 >= 256) {
                            // dense x dense
                            float2 sum_upper = make_float2(0, 0);
                            float2 sum_lower = make_float2(0, 0);

                            #if 1
                            for (int j1 = 0, colmask1 = 1; j1 < octile_w && j1 < g1.n_node - J1; ++j1, colmask1 <<= 1) {
                                auto e1_upper = octile1(i1_upper, j1);
                                auto e1_lower = octile1(i1_lower, j1);
                                bool m1_upper = o1.nzmask_r_bytes[i1_upper] & colmask1;
                                bool m1_lower = o1.nzmask_r_bytes[i1_lower] & colmask1;
                    
                                #pragma unroll (octile_w)
                                for (int j2 = 0, colmask2 = 1; j2 < octile_w; ++j2, colmask2 <<= 1) {
                                    if (o2.nzmask_r_bytes[i2] & colmask2) {
                                        auto e2 = octile2(i2, j2);
                                        auto r  = rhs(j1, j2);
                                        sum_upper.x -= r.x * (m1_upper ? edge_kernel(e1_upper, e2) : 0.f);
                                        sum_upper.y -= r.y * (m1_upper ? edge_kernel(e1_upper, e2) : 0.f);
                                        sum_lower.x -= r.x * (m1_lower ? edge_kernel(e1_lower, e2) : 0.f);
                                        sum_lower.y -= r.y * (m1_lower ? edge_kernel(e1_lower, e2) : 0.f);
                                    }
                                }
                            }
                            #else
                            for (int j1 = 0; j1 < octile_w && j1 < g1.n_node - J1; ++j1) {
                                auto e1_upper = octile1 (i1_upper, j1);
                                auto e1_lower = octile1 (i1_lower, j1);
                                auto m1_upper = 1ULL << (i1_upper + j1 * octile_h);
                                auto m1_lower = 1ULL << (i1_lower + j1 * octile_h);
                    
                                #pragma unroll (octile_w)
                                for (int j2 = 0, mask = 1; j2 < octile_w; ++j2, mask <<= 1) {
                                    auto e2 = octile2 (i2, j2);
                                    auto r  = rhs (j1, j2);
                                    auto m2 = 1ULL << (i2 + j2 * octile_h);
                                    if ((o1.nzmask & m1_upper) && (o2.nzmask & m2)) {
                                        sum_upper -= edge_kernel(e1_upper, e2) * r;
                                    }
                                    if ((o1.nzmask & m1_lower) && (o2.nzmask & m2)) {
                                        sum_lower -= edge_kernel(e1_lower, e2) * r ;
                                    }
                                }
                            }
                            #endif

                            atomicAdd(&scratch.Ap((I1 + i1_upper) * n2 + (I2 + i2)), sum_upper.x);
                            atomicAdd(&scratch.Ap((I1 + i1_lower) * n2 + (I2 + i2)), sum_lower.x);
                            atomicAdd(&scratch.Ap((I1 + i1_upper) * n2 + (I2 + i2) + N), sum_upper.y);
                            atomicAdd(&scratch.Ap((I1 + i1_lower) * n2 + (I2 + i2) + N), sum_lower.y);

                        } else {
                            // sparse x sparse
                            nzlist nzlist1 {cache + p1 * shmem_bytes_per_warp + octile::size_bytes};
                            nzlist nzlist2 {cache + p2 * shmem_bytes_per_warp + octile::size_bytes + nzlist::size_bytes + octile::size_bytes};

                            for (int i = lane; i < nnz1 * nnz2; i += warp_size) {
                                int  k1 = i / nnz2;
                                int  k2 = i - k1 * nnz2;
                                int  p1 = nzlist1(k1);
                                int  p2 = nzlist2(k2);
                                int  i1 = p1 % octile_h;
                                int  j1 = p1 / octile_h;
                                int  i2 = p2 % octile_h;
                                int  j2 = p2 / octile_h;
                                auto e1 = octile1(p1);
                                auto e2 = octile2(p2);
                                auto r  = rhs(j1, j2);
                                auto e  = -edge_kernel(e1, e2);
                                atomicAdd(&scratch.Ap((I1 + i1) * n2 + (I2 + i2)    ), e * r.x);
                                atomicAdd(&scratch.Ap((I1 + i1) * n2 + (I2 + i2) + N), e * r.y);
                            }
                        }
                    }

                    __syncthreads();
                }
            }

            __syncthreads();

            // alpha = rTr / dot( p, Ap );
            auto pAp   = block_vdotv(scratch.p(), scratch.Ap(), 2 * N);
            auto alpha = rTz / pAp;

            // x = x + alpha * p;
            // r = r - alpha * Ap;
            // z = M^-1 . r
            //   = (Dx . Vx^-1)^-1 . r
            //   = Vx . r ./ Dx
            // rTr      = r^T . r
            // rTz_next = r^T . z
            float rTr = 0, rTz_next = 0;
            for (int i = threadIdx.x; i < N; i += blockDim.x) {
                const int i1 = i / n2;
                const int i2 = i % n2;
                const float d1 = g1.degree[i1] / (1 - q);
                const float d2 = g2.degree[i2] / (1 - q);
                const float dx = d1 * d2;
                const float vx = node_kernel(g1.node[i1], g2.node[i2]);

                #pragma unroll 2
                for(int k = 0; k < 2; ++k) {
                    scratch.x(i + k * N) += alpha * scratch.p(i + k * N);
                    scratch.r(i + k * N) -= alpha * scratch.Ap(i + k * N);
                    scratch.z(i + k * N)  = vx / dx * scratch.r(i + k * N);
                    rTr      += scratch.r(i + k * N) * scratch.r(i + k * N);
                    rTz_next += scratch.r(i + k * N) * scratch.z(i + k * N);
                }
            }

            // rTr      = block_sum(rTr);
            // rTz_next = block_sum(rTz_next);
            __shared__ float sum1, sum2;
            if (threadIdx.x == 0) sum1 = 0, sum2 = 0;
            #pragma unroll
            for (int p = (warp_size >> 1); p >= 1; p >>= 1) {
                rTr      += __shfl_xor_sync(0xFFFFFFFF, rTr, p);
                rTz_next += __shfl_xor_sync(0xFFFFFFFF, rTz_next, p);
            }
            __syncthreads();
            if (laneid() == 0) {
                atomicAdd(&sum1, rTr);
                atomicAdd(&sum2, rTz_next);
            }
            __syncthreads();
            rTr      = sum1;
            rTz_next = sum2;

            if (sqrtf(rTr) < 1e-10f * 2 * N) break;

            // beta = rTz_next / rTz;
            auto beta = rTz_next / rTz;

            // p = r + beta * p;
            for (int i = threadIdx.x; i < 2 * N; i += blockDim.x) {
                scratch.p(i) = scratch.z(i) + beta * scratch.p(i);
            }
            __syncthreads();

            rTz = rTz_next;
        }

        #if 0
        __syncthreads();
        float R = 0;
        for (int i = threadIdx.x; i < N; i += blockDim.x) {
            R += scratch.x (i);
        }
        R = warp_sum (R);
        __shared__ float block_R;
        if (threadIdx.x == 0) block_R = 0;
        __syncthreads();
        if (laneid() == 0) atomicAdd (&block_R, R);
        __syncthreads();
        if (threadIdx.x == 0) {
            printf ("sum(R) = %.7f\n", block_R);
            printf ("Converged after %d iterations\n", k);
            for (int ij = 0; ij < N; ++ij) {
                printf ("solution x[%d] = %.7f\n", ij, scratch.x (ij));
            }
        }
        __syncthreads();
        #endif
    }

    template<class StartingProbability>
    __inline__ __device__ static void derivative_p(
        StartingProbability const p_start,
        Graph const    g1,
        Graph const    g2,
        pcg_scratch_t  scratch,
        char * const   cache,
        float * const  dK) {
    
        using namespace graphdot::cuda;
    
        const int lane = laneid();
        const int n1   = g1.n_node;
        const int n2   = g2.n_node;
        const int N    = n1 * n2;
    
        array_t<float, StartingProbability::jac_dims> dKdp_local;
        #pragma unroll (StartingProbability::jac_dims)
        for(int i = 0; i < StartingProbability::jac_dims; ++i) {
            dKdp_local[i] = 0;
        }
    
        for (int i = threadIdx.x; i < N; i += blockDim.x) {
            const int i1 = i / n2;
            const int i2 = i % n2;
            const auto n1 = g1.node[i1];
            const auto n2 = g2.node[i2];
            const float p1 = p_start(n1);
            const float p2 = p_start(n2);
            const float r = scratch.x(i);
    
            array_t<float, StartingProbability::jac_dims> jac1, jac2;
            p_start._j_a_c_o_b_i_a_n_(jac1, n1);
            p_start._j_a_c_o_b_i_a_n_(jac2, n2);

            #pragma unroll (StartingProbability::jac_dims)
            for(int j = 0; j < StartingProbability::jac_dims; ++j) {
                dKdp_local[j] += (jac1[j] * p2 + p1 * jac2[j]) * r;
            }
        }
    
        #pragma unroll (StartingProbability::jac_dims)
        for(int j = 0; j < StartingProbability::jac_dims; ++j) {
            dKdp_local[j] = warp_sum(dKdp_local[j]);
            if (lane == 0) atomicAdd(dK + j, dKdp_local[j]);
        }
    }
    
    template<class NodeKernel, class StartingProbability>
    __inline__ __device__ static void derivative_q(
        NodeKernel const node_kernel,
        StartingProbability const p_start,
        Graph const    g1,
        Graph const    g2,
        scratch_t      scratch,
        char * const   cache,
        float * const  dK,
        const float    q) {

        using namespace graphdot::cuda;

        const int lane = laneid();
        const int n1   = g1.n_node;
        const int n2   = g2.n_node;
        const int N    = n1 * n2;

        float dq_local = 0;

        float rrq = 1.0f / (1.0f - q);
        float rrq3 = rrq * rrq * rrq;

        for (int i = threadIdx.x; i < N; i += blockDim.x) {
            const int i1 = i / n2;
            const int i2 = i % n2;
            const auto n1 = g1.node[i1];
            const auto n2 = g2.node[i2];
            const float rd1 = g1.degree[i1];// / (1 - q);
            const float rd2 = g2.degree[i2];// / (1 - q);
            const float rdx = rd1 * rd2;        
            const float YDq = scratch.x(i);
            const float Yp  = scratch.x(i + N);
            const float v = node_kernel(n1, n2);

            dq_local += 2 * rrq * p_start(n1) * p_start(n2) * YDq - 2 * rrq3 * Yp * rdx / v * YDq;
        }

        dq_local = warp_sum(dq_local);
        if (lane == 0) atomicAdd(dK, dq_local);
    }

    template<class NodeKernel>
    __inline__ __device__ static void derivative_node(
        NodeKernel const node_kernel,
        Graph const    g1,
        Graph const    g2,
        scratch_t      scratch,
        char * const   cache,
        float * const  dK,
        const float    q) {

        using namespace graphdot::cuda;

        const int lane = laneid();
        const int n1   = g1.n_node;
        const int n2   = g2.n_node;
        const int N    = n1 * n2;

        float dK_local[NodeKernel::jac_dims];
        #pragma unroll (NodeKernel::jac_dims)
        for(int i = 0; i < NodeKernel::jac_dims; ++i) {
            dK_local[i] = 0;
        }

        for (int i = threadIdx.x; i < N; i += blockDim.x) {
            const int i1 = i / n2;
            const int i2 = i % n2;
            const auto n1 = g1.node[i1];
            const auto n2 = g2.node[i2];
            const float d1 = g1.degree[i1] / (1 - q);
            const float d2 = g2.degree[i2] / (1 - q);
            const float dx = d1 * d2;        
            const float YDq = scratch.x(i);
            const float Yp  = scratch.x(i + N);
            const float dK_dZ = -dx * Yp * YDq;

            const float v = node_kernel(n1, n2);
            float jac[NodeKernel::jac_dims];
            node_kernel._j_a_c_o_b_i_a_n_(jac, n1, n2);
            #pragma unroll (NodeKernel::jac_dims)
            for(int j = 0; j < NodeKernel::jac_dims; ++j) {
                dK_local[j] += -dK_dZ / (v * v) * jac[j];
            }
        }

        #pragma unroll (NodeKernel::jac_dims)
        for(int j = 0; j < NodeKernel::jac_dims; ++j) {
            dK_local[j] = warp_sum(dK_local[j]);
            if (lane == 0) atomicAdd(dK + j, dK_local[j]);
        }
    }

    template<class EdgeKernel>
    __inline__ __device__ static void derivative_edge(
        EdgeKernel const edge_kernel,
        Graph const    g1,
        Graph const    g2,
        scratch_t      scratch,
        char * const   cache,
        float * const  dK) {

        using namespace graphdot::cuda;

        const int warp_id_local  = threadIdx.x / warp_size;
        const int warp_num_local = blockDim.x / warp_size;
        const int lane           = laneid();
        const int n1             = g1.n_node;
        const int n2             = g2.n_node;
        const int N              = n1 * n2;
        const int i1_upper       =  lane              / octile_h;
        const int i1_lower       = (lane + warp_size) / octile_h;
        const int i2             =  lane              % octile_h;

        octile octilex {cache
                        + warp_id_local * shmem_bytes_per_warp
                        + octile::size_bytes * 2
                        + nzlist::size_bytes * 2};

        float dK_local[EdgeKernel::jac_dims];
        #pragma unroll (EdgeKernel::jac_dims)
        for(int i = 0; i < EdgeKernel::jac_dims; ++i) {
            dK_local[i] = 0;
        }

        #if 1
        for (int O1 = 0; O1 < g1.n_octile; O1 += warp_num_local) {

            const int nt1 = min(g1.n_octile - O1, warp_num_local);

            if (warp_id_local < nt1) {
                // load the first submatrix in compact format into shared memory
                octile octile1 {cache + warp_id_local * shmem_bytes_per_warp};
                nzlist nzlist1 {cache + warp_id_local * shmem_bytes_per_warp + octile::size_bytes};
                load(lane, g1.octile[O1 + warp_id_local], octile1, nzlist1, octilex);
            }

            __syncthreads();

            for (int O2 = 0; O2 < g2.n_octile; O2 += warp_num_local) {

                const int nt2 = min(g2.n_octile - O2, warp_num_local);

                if (warp_id_local < nt2) {
                    // load the second submatrix in compact fornat into shared memory
                    octile octile2 {cache + warp_id_local * shmem_bytes_per_warp + octile::size_bytes + nzlist::size_bytes};
                    nzlist nzlist2 {cache + warp_id_local * shmem_bytes_per_warp + octile::size_bytes + nzlist::size_bytes + octile::size_bytes};
                    load(lane, g2.octile[O2 + warp_id_local], octile2, nzlist2, octilex);
                }

                __syncthreads();

                for (int t = warp_id_local; t < nt1 * nt2; t += warp_num_local) {

                    const int p1 = t / nt2;
                    const int p2 = t % nt2;

                    const auto o1  = g1.octile[O1 + p1];
                    const auto o2  = g2.octile[O2 + p2];
                    const int nnz1 = __popcll(o1.nzmask);
                    const int nnz2 = __popcll(o2.nzmask);
                    const int I1   = o1.upper;
                    const int J1   = o1.left;
                    const int I2   = o2.upper;
                    const int J2   = o2.left;

                    octile octile1 {cache + p1 * shmem_bytes_per_warp};
                    octile octile2 {cache + p2 * shmem_bytes_per_warp + octile::size_bytes + nzlist::size_bytes};
                    // rhs    rhs     {cache + warp_id_local * shmem_bytes_per_warp + octile::size_bytes * 2 + nzlist::size_bytes * 2};
                    float * YDq = (float *)(cache + warp_id_local * shmem_bytes_per_warp + octile::size_bytes * 2 + nzlist::size_bytes * 2);
                    float * Yp  = YDq + octile_w * octile_w;

                    // load dY
                    {
                        int j1 = lane / octile_w;
                        int j2 = lane % octile_w;
                        if (J1 + j1                        < n1 && J2 + j2 < n2) YDq[lane            ] = scratch.x((J1 + j1                       ) * n2 + (J2 + j2));
                        if (J1 + j1 + warp_size / octile_w < n1 && J2 + j2 < n2) YDq[lane + warp_size] = scratch.x((J1 + j1 + warp_size / octile_w) * n2 + (J2 + j2));
                    }
                    {
                        int i1 = lane / octile_h;
                        int i2 = lane % octile_h;
                        if (I1 + i1                        < n1 && I2 + i2 < n2) Yp[lane            ] = scratch.x((I1 + i1                       ) * n2 + (I2 + i2) + N);
                        if (I1 + i1 + warp_size / octile_w < n1 && I2 + i2 < n2) Yp[lane + warp_size] = scratch.x((I1 + i1 + warp_size / octile_w) * n2 + (I2 + i2) + N);
                    }

                    if (nnz1 * nnz2 >= 256) {
                        // dense x dense
                        for (int j1 = 0, colmask1 = 1; j1 < octile_w && j1 < g1.n_node - J1; ++j1, colmask1 <<= 1) {
                            auto e1_upper = octile1(i1_upper, j1);
                            auto e1_lower = octile1(i1_lower, j1);
                            bool m1_upper = o1.nzmask_r_bytes[i1_upper] & colmask1;
                            bool m1_lower = o1.nzmask_r_bytes[i1_lower] & colmask1;
                
                            #pragma unroll (octile_w)
                            for (int j2 = 0, colmask2 = 1; j2 < octile_w; ++j2, colmask2 <<= 1) {
                                if (o2.nzmask_r_bytes[i2] & colmask2) {
                                    auto e2 = octile2(i2, j2);
                                    const float dK_dY_upper = -Yp[i1_upper * octile_h + i2] * YDq[j1 * octile_w + j2];
                                    const float dK_dY_lower = -Yp[i1_lower * octile_h + i2] * YDq[j1 * octile_w + j2];
                                    float jac_upper[EdgeKernel::jac_dims];
                                    float jac_lower[EdgeKernel::jac_dims];
                                    if (m1_upper) edge_kernel._j_a_c_o_b_i_a_n_(jac_upper, e1_upper, e2);
                                    if (m1_lower) edge_kernel._j_a_c_o_b_i_a_n_(jac_lower, e1_lower, e2);
                                    #pragma unroll (EdgeKernel::jac_dims)
                                    for(int j = 0; j < EdgeKernel::jac_dims; ++j) {
                                        dK_local[j] -=
                                            dK_dY_upper * (m1_upper ? jac_upper[j] : 0.f) + 
                                            dK_dY_lower * (m1_lower ? jac_lower[j] : 0.f);
                                    }
                                }
                            }
                        }
                    }
                     else {
                        // sparse x sparse
                        nzlist nzlist1 {cache + p1 * shmem_bytes_per_warp + octile::size_bytes};
                        nzlist nzlist2 {cache + p2 * shmem_bytes_per_warp + octile::size_bytes + nzlist::size_bytes + octile::size_bytes};

                        for (int i = lane; i < nnz1 * nnz2; i += warp_size) {
                            int  k1 = i / nnz2;
                            int  k2 = i - k1 * nnz2;
                            int  p1 = nzlist1(k1);
                            int  p2 = nzlist2(k2);
                            int  i1 = p1 % octile_h;
                            int  j1 = p1 / octile_h;
                            int  i2 = p2 % octile_h;
                            int  j2 = p2 / octile_h;
                            auto e1 = octile1(p1);
                            auto e2 = octile2(p2);

                            const float dK_dY = -Yp[i1 * octile_h + i2] * YDq[j1 * octile_w + j2];
                            float jac[EdgeKernel::jac_dims];
                            edge_kernel._j_a_c_o_b_i_a_n_(jac, e1, e2);
                            #pragma unroll (EdgeKernel::jac_dims)
                            for(int j = 0; j < EdgeKernel::jac_dims; ++j) {
                                dK_local[j] -= dK_dY * jac[j];
                            }
                        }
                    }
                }

                __syncthreads();
            }
        }
        #endif

        #pragma unroll (EdgeKernel::jac_dims)
        for(int j = 0; j < EdgeKernel::jac_dims; ++j) {
            dK_local[j] = warp_sum(dK_local[j]);
            if (lane == 0) {
                atomicAdd(dK + j, dK_local[j]);
            }
        }
    }
};

}  // namespace marginalized

}  // namespace graphdot

#endif
