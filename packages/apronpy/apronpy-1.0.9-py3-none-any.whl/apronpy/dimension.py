"""
APRON Dimensions
================

:Author: Caterina Urban
"""
from _ctypes import Structure, POINTER
from ctypes import c_uint, c_size_t

from apronpy.cdll import libapron, libc


class Dim(c_uint):

    def __repr__(self):
        return str(self.value)

    def __lt__(self, other: 'Dim'):
        assert isinstance(other, Dim)
        return self.value < other.value

    def __le__(self, other: 'Dim'):
        assert isinstance(other, Dim)
        return self.__lt__(other) or self.__eq__(other)

    def __eq__(self, other: 'Dim'):
        assert isinstance(other, Dim)
        return self.value == other.value

    def __ne__(self, other: 'Dim'):
        assert isinstance(other, Dim)
        return not self.__eq__(other)

    def __ge__(self, other: 'Dim'):
        assert isinstance(other, Dim)
        return self.__gt__(other) or self.__eq__(other)

    def __gt__(self, other: 'Dim'):
        assert isinstance(other, Dim)
        return self.value > other.value


AP_DIM_MAX = Dim(c_uint(-1).value)


class Dimension(Structure):
    """
    typedef struct ap_dimension_t {
      size_t intdim;
      size_t realdim;
    } ap_dimension_t;
    """

    _fields_ = [
        ('intdim', c_size_t),
        ('realdim', c_size_t)
    ]


class DimChange(Structure):
    """
    typedef struct ap_dimchange_t {
      ap_dim_t* dim;  /* Assumed to be an array of size intdim+realdim */
      size_t intdim ; /* Number of integer dimensions to add/remove */
      size_t realdim; /* Number of real dimensions to add/remove */
    } ap_dimchange_t;
    """

    _fields_ = [
        ('dim', POINTER(Dim)),
        ('intdim', c_size_t),
        ('realdim', c_size_t)
    ]


class PyDimChange:

    def __init__(self, intdim, realdim):
        self.dimchange = libapron.ap_dimchange_alloc(intdim, realdim)

    def __del__(self):
        if self.dimchange.contents.dim:
           libc.free(self.dimchange.contents.dim)
        self.dimchange.contents.indim = 0
        self.dimchange.contents.realdim = 0
        self.dimchange.contents.dim = None
        libc.free(self.dimchange)

    @property
    def _as_parameter_(self):
        return self.dimchange

    @staticmethod
    def from_param(argument):
        assert isinstance(argument, PyDimChange)
        return argument


libapron.ap_dimchange_alloc.argtypes = [c_size_t, c_size_t]
libapron.ap_dimchange_alloc.restype = POINTER(DimChange)


class DimChange2(Structure):
    """
    typedef struct ap_dimchange2_t {
      ap_dimchange_t* add;    /* If not NULL, specifies the adding new dimensions */
      ap_dimchange_t* remove; /* If not NULL, specifies the removal of dimensions */
    } ap_dimchange2_t;
    """

    _fields_ = [
        ('add', POINTER(DimChange)),
        ('remove', POINTER(DimChange))
    ]


class DimPerm(Structure):
    """
    typedef struct ap_dimperm_t {
      ap_dim_t* dim;    /* Array assumed to be of size size */
      size_t size;
    } ap_dimperm_t;
    """

    _fields_ = [
        ('dim', POINTER(Dim)),
        ('size', c_size_t)
    ]
