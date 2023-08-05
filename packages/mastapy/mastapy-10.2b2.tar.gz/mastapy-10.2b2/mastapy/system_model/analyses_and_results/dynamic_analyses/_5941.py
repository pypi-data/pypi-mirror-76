'''_5941.py

ZerolBevelGearSetDynamicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2114
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6238
from mastapy.system_model.analyses_and_results.dynamic_analyses import _5939, _5940, _5835
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_SET_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'ZerolBevelGearSetDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearSetDynamicAnalysis',)


class ZerolBevelGearSetDynamicAnalysis(_5835.BevelGearSetDynamicAnalysis):
    '''ZerolBevelGearSetDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_SET_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearSetDynamicAnalysis.TYPE'):
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
    def zerol_bevel_gears_dynamic_analysis(self) -> 'List[_5939.ZerolBevelGearDynamicAnalysis]':
        '''List[ZerolBevelGearDynamicAnalysis]: 'ZerolBevelGearsDynamicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearsDynamicAnalysis, constructor.new(_5939.ZerolBevelGearDynamicAnalysis))
        return value

    @property
    def zerol_bevel_meshes_dynamic_analysis(self) -> 'List[_5940.ZerolBevelGearMeshDynamicAnalysis]':
        '''List[ZerolBevelGearMeshDynamicAnalysis]: 'ZerolBevelMeshesDynamicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelMeshesDynamicAnalysis, constructor.new(_5940.ZerolBevelGearMeshDynamicAnalysis))
        return value
