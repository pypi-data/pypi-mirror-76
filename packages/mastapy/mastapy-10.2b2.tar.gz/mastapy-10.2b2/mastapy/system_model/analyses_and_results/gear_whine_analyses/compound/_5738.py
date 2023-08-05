'''_5738.py

FaceGearSetCompoundGearWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2089
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.gear_whine_analyses.compound import _5736, _5737, _5742
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5336
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_SET_COMPOUND_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.Compound', 'FaceGearSetCompoundGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearSetCompoundGearWhineAnalysis',)


class FaceGearSetCompoundGearWhineAnalysis(_5742.GearSetCompoundGearWhineAnalysis):
    '''FaceGearSetCompoundGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_SET_COMPOUND_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearSetCompoundGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2089.FaceGearSet':
        '''FaceGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2089.FaceGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2089.FaceGearSet':
        '''FaceGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2089.FaceGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def face_gears_compound_gear_whine_analysis(self) -> 'List[_5736.FaceGearCompoundGearWhineAnalysis]':
        '''List[FaceGearCompoundGearWhineAnalysis]: 'FaceGearsCompoundGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearsCompoundGearWhineAnalysis, constructor.new(_5736.FaceGearCompoundGearWhineAnalysis))
        return value

    @property
    def face_meshes_compound_gear_whine_analysis(self) -> 'List[_5737.FaceGearMeshCompoundGearWhineAnalysis]':
        '''List[FaceGearMeshCompoundGearWhineAnalysis]: 'FaceMeshesCompoundGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceMeshesCompoundGearWhineAnalysis, constructor.new(_5737.FaceGearMeshCompoundGearWhineAnalysis))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_5336.FaceGearSetGearWhineAnalysis]':
        '''List[FaceGearSetGearWhineAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5336.FaceGearSetGearWhineAnalysis))
        return value

    @property
    def assembly_gear_whine_analysis_load_cases(self) -> 'List[_5336.FaceGearSetGearWhineAnalysis]':
        '''List[FaceGearSetGearWhineAnalysis]: 'AssemblyGearWhineAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyGearWhineAnalysisLoadCases, constructor.new(_5336.FaceGearSetGearWhineAnalysis))
        return value
