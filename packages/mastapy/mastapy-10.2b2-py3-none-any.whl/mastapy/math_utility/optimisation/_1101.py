'''_1101.py

Optimisable
'''


from mastapy.math_utility.optimisation import _1097
from mastapy._internal.python_net import python_net_import

_OPTIMISABLE = python_net_import('SMT.MastaAPI.MathUtility.Optimisation', 'Optimisable')


__docformat__ = 'restructuredtext en'
__all__ = ('Optimisable',)


class Optimisable(_1097.AbstractOptimisable):
    '''Optimisable

    This is a mastapy class.
    '''

    TYPE = _OPTIMISABLE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'Optimisable.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
