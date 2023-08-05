#ifndef GRAPHDOT_VIEW_H_
#define GRAPHDOT_VIEW_H_

#include <type_traits>
#include "array.h"

namespace graphdot {

template<class type, int ndim>
struct view {
    using size_type = std::int32_t;
    using element_type = std::remove_const_t<type>;
    using pointer_type = std::add_pointer_t<element_type>;
    constexpr static size_type

    pointer_type _ptr;
    array<size_type, ndim> _shape, _stride;

    template<class ...Ts>
    __host__ __device__ __inline__
    array(pointer_type ptr, tuple<Ts...> shape, tuple<Ts...> stride) :
        _ptr(ptr),
        _shape(shape),
        _stride(stride) {
        static_assert(ndim == sizeof...(Ts));
    }

    template<class T>
    __host__ __device__ __inline__
    array(T const value) {
        #pragma unroll (size)
        for(int i = 0; i < size; ++i) {
            _data[i] = value;
        }
    }

    __host__ __device__ __inline__
    array & operator = (array const & other) {
        #pragma unroll (size)
        for(int i = 0; i < size; ++i) {
            _data[i] = other._data[i];
        }
        return *this;
    }

    __host__ __device__ __inline__
    element_type & operator [] (int i) {return _data[i];}
};

}

#endif
