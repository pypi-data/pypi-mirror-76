﻿'''_5048.py

HypoidGearSetMultiBodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2095
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6159
from mastapy.system_model.analyses_and_results.mbd_analyses import _5047, _5046, _4991
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_SET_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'HypoidGearSetMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearSetMultiBodyDynamicsAnalysis',)


class HypoidGearSetMultiBodyDynamicsAnalysis(_4991.AGMAGleasonConicalGearSetMultiBodyDynamicsAnalysis):
    '''HypoidGearSetMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR_SET_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGearSetMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2095.HypoidGearSet':
        '''HypoidGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2095.HypoidGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6159.HypoidGearSetLoadCase':
        '''HypoidGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6159.HypoidGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def gears(self) -> 'List[_5047.HypoidGearMultiBodyDynamicsAnalysis]':
        '''List[HypoidGearMultiBodyDynamicsAnalysis]: 'Gears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Gears, constructor.new(_5047.HypoidGearMultiBodyDynamicsAnalysis))
        return value

    @property
    def hypoid_gears_multi_body_dynamics_analysis(self) -> 'List[_5047.HypoidGearMultiBodyDynamicsAnalysis]':
        '''List[HypoidGearMultiBodyDynamicsAnalysis]: 'HypoidGearsMultiBodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearsMultiBodyDynamicsAnalysis, constructor.new(_5047.HypoidGearMultiBodyDynamicsAnalysis))
        return value

    @property
    def hypoid_meshes_multi_body_dynamics_analysis(self) -> 'List[_5046.HypoidGearMeshMultiBodyDynamicsAnalysis]':
        '''List[HypoidGearMeshMultiBodyDynamicsAnalysis]: 'HypoidMeshesMultiBodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidMeshesMultiBodyDynamicsAnalysis, constructor.new(_5046.HypoidGearMeshMultiBodyDynamicsAnalysis))
        return value
