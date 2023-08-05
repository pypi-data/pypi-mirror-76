'''_574.py

ConicalPinionMicroGeometryConfig
'''


from mastapy.gears.manufacturing.bevel import _568, _562
from mastapy._internal import constructor
from mastapy._internal.python_net import python_net_import

_CONICAL_PINION_MICRO_GEOMETRY_CONFIG = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Bevel', 'ConicalPinionMicroGeometryConfig')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalPinionMicroGeometryConfig',)


class ConicalPinionMicroGeometryConfig(_562.ConicalGearMicroGeometryConfig):
    '''ConicalPinionMicroGeometryConfig

    This is a mastapy class.
    '''

    TYPE = _CONICAL_PINION_MICRO_GEOMETRY_CONFIG

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConicalPinionMicroGeometryConfig.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def pinion_concave_ob_configuration(self) -> '_568.ConicalMeshFlankNurbsMicroGeometryConfig':
        '''ConicalMeshFlankNurbsMicroGeometryConfig: 'PinionConcaveOBConfiguration' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_568.ConicalMeshFlankNurbsMicroGeometryConfig)(self.wrapped.PinionConcaveOBConfiguration) if self.wrapped.PinionConcaveOBConfiguration else None

    @property
    def pinion_convex_ib_configuration(self) -> '_568.ConicalMeshFlankNurbsMicroGeometryConfig':
        '''ConicalMeshFlankNurbsMicroGeometryConfig: 'PinionConvexIBConfiguration' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_568.ConicalMeshFlankNurbsMicroGeometryConfig)(self.wrapped.PinionConvexIBConfiguration) if self.wrapped.PinionConvexIBConfiguration else None
