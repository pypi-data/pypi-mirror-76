'''_4276.py

CylindricalGearSetModalAnalysisAtAStiffness
'''


from typing import List

from mastapy.system_model.part_model.gears import _2086
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6119
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4275, _4274, _4287
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_SET_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness', 'CylindricalGearSetModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearSetModalAnalysisAtAStiffness',)


class CylindricalGearSetModalAnalysisAtAStiffness(_4287.GearSetModalAnalysisAtAStiffness):
    '''CylindricalGearSetModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_SET_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearSetModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2086.CylindricalGearSet':
        '''CylindricalGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2086.CylindricalGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6119.CylindricalGearSetLoadCase':
        '''CylindricalGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6119.CylindricalGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def cylindrical_gears_modal_analysis_at_a_stiffness(self) -> 'List[_4275.CylindricalGearModalAnalysisAtAStiffness]':
        '''List[CylindricalGearModalAnalysisAtAStiffness]: 'CylindricalGearsModalAnalysisAtAStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearsModalAnalysisAtAStiffness, constructor.new(_4275.CylindricalGearModalAnalysisAtAStiffness))
        return value

    @property
    def cylindrical_meshes_modal_analysis_at_a_stiffness(self) -> 'List[_4274.CylindricalGearMeshModalAnalysisAtAStiffness]':
        '''List[CylindricalGearMeshModalAnalysisAtAStiffness]: 'CylindricalMeshesModalAnalysisAtAStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalMeshesModalAnalysisAtAStiffness, constructor.new(_4274.CylindricalGearMeshModalAnalysisAtAStiffness))
        return value
