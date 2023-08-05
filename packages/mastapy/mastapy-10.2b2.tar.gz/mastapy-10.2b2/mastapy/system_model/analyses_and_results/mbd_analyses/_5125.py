'''_5125.py

ZerolBevelGearSetMultiBodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2114
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6238
from mastapy.system_model.analyses_and_results.mbd_analyses import _5124, _5123, _5005
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_SET_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'ZerolBevelGearSetMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearSetMultiBodyDynamicsAnalysis',)


class ZerolBevelGearSetMultiBodyDynamicsAnalysis(_5005.BevelGearSetMultiBodyDynamicsAnalysis):
    '''ZerolBevelGearSetMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_SET_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearSetMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2114.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2114.ZerolBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6238.ZerolBevelGearSetLoadCase':
        '''ZerolBevelGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6238.ZerolBevelGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def gears(self) -> 'List[_5124.ZerolBevelGearMultiBodyDynamicsAnalysis]':
        '''List[ZerolBevelGearMultiBodyDynamicsAnalysis]: 'Gears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Gears, constructor.new(_5124.ZerolBevelGearMultiBodyDynamicsAnalysis))
        return value

    @property
    def zerol_bevel_gears_multi_body_dynamics_analysis(self) -> 'List[_5124.ZerolBevelGearMultiBodyDynamicsAnalysis]':
        '''List[ZerolBevelGearMultiBodyDynamicsAnalysis]: 'ZerolBevelGearsMultiBodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearsMultiBodyDynamicsAnalysis, constructor.new(_5124.ZerolBevelGearMultiBodyDynamicsAnalysis))
        return value

    @property
    def zerol_bevel_meshes_multi_body_dynamics_analysis(self) -> 'List[_5123.ZerolBevelGearMeshMultiBodyDynamicsAnalysis]':
        '''List[ZerolBevelGearMeshMultiBodyDynamicsAnalysis]: 'ZerolBevelMeshesMultiBodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelMeshesMultiBodyDynamicsAnalysis, constructor.new(_5123.ZerolBevelGearMeshMultiBodyDynamicsAnalysis))
        return value
