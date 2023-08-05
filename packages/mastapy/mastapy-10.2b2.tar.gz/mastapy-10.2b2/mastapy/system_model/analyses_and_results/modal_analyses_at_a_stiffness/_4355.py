'''_4355.py

ZerolBevelGearSetModalAnalysisAtAStiffness
'''


from typing import List

from mastapy.system_model.part_model.gears import _2114
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6238
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4354, _4353, _4249
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_SET_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness', 'ZerolBevelGearSetModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearSetModalAnalysisAtAStiffness',)


class ZerolBevelGearSetModalAnalysisAtAStiffness(_4249.BevelGearSetModalAnalysisAtAStiffness):
    '''ZerolBevelGearSetModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_SET_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearSetModalAnalysisAtAStiffness.TYPE'):
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
    def zerol_bevel_gears_modal_analysis_at_a_stiffness(self) -> 'List[_4354.ZerolBevelGearModalAnalysisAtAStiffness]':
        '''List[ZerolBevelGearModalAnalysisAtAStiffness]: 'ZerolBevelGearsModalAnalysisAtAStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearsModalAnalysisAtAStiffness, constructor.new(_4354.ZerolBevelGearModalAnalysisAtAStiffness))
        return value

    @property
    def zerol_bevel_meshes_modal_analysis_at_a_stiffness(self) -> 'List[_4353.ZerolBevelGearMeshModalAnalysisAtAStiffness]':
        '''List[ZerolBevelGearMeshModalAnalysisAtAStiffness]: 'ZerolBevelMeshesModalAnalysisAtAStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelMeshesModalAnalysisAtAStiffness, constructor.new(_4353.ZerolBevelGearMeshModalAnalysisAtAStiffness))
        return value
