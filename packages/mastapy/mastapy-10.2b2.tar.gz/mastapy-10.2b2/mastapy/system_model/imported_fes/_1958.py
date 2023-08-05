﻿'''_1958.py

ImportedFeLinkWithSelection
'''


from typing import Callable

from mastapy._internal import constructor
from mastapy.system_model.imported_fes import (
    _1926, _1955, _1956, _1957,
    _1959, _1960, _1961, _1962,
    _1963, _1964, _1965, _1977,
    _1988, _1989
)
from mastapy._internal.cast_exception import CastException
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_IMPORTED_FE_LINK_WITH_SELECTION = python_net_import('SMT.MastaAPI.SystemModel.ImportedFEs', 'ImportedFeLinkWithSelection')


__docformat__ = 'restructuredtext en'
__all__ = ('ImportedFeLinkWithSelection',)


class ImportedFeLinkWithSelection(_0.APIBase):
    '''ImportedFeLinkWithSelection

    This is a mastapy class.
    '''

    TYPE = _IMPORTED_FE_LINK_WITH_SELECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ImportedFeLinkWithSelection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def add_selected_nodes(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'AddSelectedNodes' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AddSelectedNodes

    @property
    def delete_all_nodes(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'DeleteAllNodes' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.DeleteAllNodes

    @property
    def select_component(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'SelectComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SelectComponent

    @property
    def link(self) -> '_1926.ImportedFELink':
        '''ImportedFELink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1926.ImportedFELink)(self.wrapped.Link) if self.wrapped.Link else None

    @property
    def link_of_type_imported_fe_electric_machine_stator_link(self) -> '_1955.ImportedFEElectricMachineStatorLink':
        '''ImportedFEElectricMachineStatorLink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1955.ImportedFEElectricMachineStatorLink.TYPE not in self.wrapped.Link.__class__.__mro__:
            raise CastException('Failed to cast link to ImportedFEElectricMachineStatorLink. Expected: {}.'.format(self.wrapped.Link.__class__.__qualname__))

        return constructor.new(_1955.ImportedFEElectricMachineStatorLink)(self.wrapped.Link) if self.wrapped.Link else None

    @property
    def link_of_type_imported_fe_gear_mesh_link(self) -> '_1956.ImportedFEGearMeshLink':
        '''ImportedFEGearMeshLink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1956.ImportedFEGearMeshLink.TYPE not in self.wrapped.Link.__class__.__mro__:
            raise CastException('Failed to cast link to ImportedFEGearMeshLink. Expected: {}.'.format(self.wrapped.Link.__class__.__qualname__))

        return constructor.new(_1956.ImportedFEGearMeshLink)(self.wrapped.Link) if self.wrapped.Link else None

    @property
    def link_of_type_imported_fe_gear_with_duplicated_meshes_link(self) -> '_1957.ImportedFEGearWithDuplicatedMeshesLink':
        '''ImportedFEGearWithDuplicatedMeshesLink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1957.ImportedFEGearWithDuplicatedMeshesLink.TYPE not in self.wrapped.Link.__class__.__mro__:
            raise CastException('Failed to cast link to ImportedFEGearWithDuplicatedMeshesLink. Expected: {}.'.format(self.wrapped.Link.__class__.__qualname__))

        return constructor.new(_1957.ImportedFEGearWithDuplicatedMeshesLink)(self.wrapped.Link) if self.wrapped.Link else None

    @property
    def link_of_type_imported_fe_multi_node_connector_link(self) -> '_1959.ImportedFEMultiNodeConnectorLink':
        '''ImportedFEMultiNodeConnectorLink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1959.ImportedFEMultiNodeConnectorLink.TYPE not in self.wrapped.Link.__class__.__mro__:
            raise CastException('Failed to cast link to ImportedFEMultiNodeConnectorLink. Expected: {}.'.format(self.wrapped.Link.__class__.__qualname__))

        return constructor.new(_1959.ImportedFEMultiNodeConnectorLink)(self.wrapped.Link) if self.wrapped.Link else None

    @property
    def link_of_type_imported_fe_multi_node_link(self) -> '_1960.ImportedFEMultiNodeLink':
        '''ImportedFEMultiNodeLink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1960.ImportedFEMultiNodeLink.TYPE not in self.wrapped.Link.__class__.__mro__:
            raise CastException('Failed to cast link to ImportedFEMultiNodeLink. Expected: {}.'.format(self.wrapped.Link.__class__.__qualname__))

        return constructor.new(_1960.ImportedFEMultiNodeLink)(self.wrapped.Link) if self.wrapped.Link else None

    @property
    def link_of_type_imported_fe_node_link(self) -> '_1961.ImportedFENodeLink':
        '''ImportedFENodeLink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1961.ImportedFENodeLink.TYPE not in self.wrapped.Link.__class__.__mro__:
            raise CastException('Failed to cast link to ImportedFENodeLink. Expected: {}.'.format(self.wrapped.Link.__class__.__qualname__))

        return constructor.new(_1961.ImportedFENodeLink)(self.wrapped.Link) if self.wrapped.Link else None

    @property
    def link_of_type_imported_fe_planetary_connector_multi_node_link(self) -> '_1962.ImportedFEPlanetaryConnectorMultiNodeLink':
        '''ImportedFEPlanetaryConnectorMultiNodeLink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1962.ImportedFEPlanetaryConnectorMultiNodeLink.TYPE not in self.wrapped.Link.__class__.__mro__:
            raise CastException('Failed to cast link to ImportedFEPlanetaryConnectorMultiNodeLink. Expected: {}.'.format(self.wrapped.Link.__class__.__qualname__))

        return constructor.new(_1962.ImportedFEPlanetaryConnectorMultiNodeLink)(self.wrapped.Link) if self.wrapped.Link else None

    @property
    def link_of_type_imported_fe_planet_based_link(self) -> '_1963.ImportedFEPlanetBasedLink':
        '''ImportedFEPlanetBasedLink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1963.ImportedFEPlanetBasedLink.TYPE not in self.wrapped.Link.__class__.__mro__:
            raise CastException('Failed to cast link to ImportedFEPlanetBasedLink. Expected: {}.'.format(self.wrapped.Link.__class__.__qualname__))

        return constructor.new(_1963.ImportedFEPlanetBasedLink)(self.wrapped.Link) if self.wrapped.Link else None

    @property
    def link_of_type_imported_fe_planet_carrier_link(self) -> '_1964.ImportedFEPlanetCarrierLink':
        '''ImportedFEPlanetCarrierLink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1964.ImportedFEPlanetCarrierLink.TYPE not in self.wrapped.Link.__class__.__mro__:
            raise CastException('Failed to cast link to ImportedFEPlanetCarrierLink. Expected: {}.'.format(self.wrapped.Link.__class__.__qualname__))

        return constructor.new(_1964.ImportedFEPlanetCarrierLink)(self.wrapped.Link) if self.wrapped.Link else None

    @property
    def link_of_type_imported_fe_point_load_link(self) -> '_1965.ImportedFEPointLoadLink':
        '''ImportedFEPointLoadLink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1965.ImportedFEPointLoadLink.TYPE not in self.wrapped.Link.__class__.__mro__:
            raise CastException('Failed to cast link to ImportedFEPointLoadLink. Expected: {}.'.format(self.wrapped.Link.__class__.__qualname__))

        return constructor.new(_1965.ImportedFEPointLoadLink)(self.wrapped.Link) if self.wrapped.Link else None

    @property
    def link_of_type_multi_angle_connection_link(self) -> '_1977.MultiAngleConnectionLink':
        '''MultiAngleConnectionLink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1977.MultiAngleConnectionLink.TYPE not in self.wrapped.Link.__class__.__mro__:
            raise CastException('Failed to cast link to MultiAngleConnectionLink. Expected: {}.'.format(self.wrapped.Link.__class__.__qualname__))

        return constructor.new(_1977.MultiAngleConnectionLink)(self.wrapped.Link) if self.wrapped.Link else None

    @property
    def link_of_type_rolling_ring_connection_link(self) -> '_1988.RollingRingConnectionLink':
        '''RollingRingConnectionLink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1988.RollingRingConnectionLink.TYPE not in self.wrapped.Link.__class__.__mro__:
            raise CastException('Failed to cast link to RollingRingConnectionLink. Expected: {}.'.format(self.wrapped.Link.__class__.__qualname__))

        return constructor.new(_1988.RollingRingConnectionLink)(self.wrapped.Link) if self.wrapped.Link else None

    @property
    def link_of_type_shaft_hub_connection_fe_link(self) -> '_1989.ShaftHubConnectionFELink':
        '''ShaftHubConnectionFELink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1989.ShaftHubConnectionFELink.TYPE not in self.wrapped.Link.__class__.__mro__:
            raise CastException('Failed to cast link to ShaftHubConnectionFELink. Expected: {}.'.format(self.wrapped.Link.__class__.__qualname__))

        return constructor.new(_1989.ShaftHubConnectionFELink)(self.wrapped.Link) if self.wrapped.Link else None
