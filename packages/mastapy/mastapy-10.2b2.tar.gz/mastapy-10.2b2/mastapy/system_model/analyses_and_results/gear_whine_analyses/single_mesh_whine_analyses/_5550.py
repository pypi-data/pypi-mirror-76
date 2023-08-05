'''_5550.py

WormGearSetSingleMeshWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2112
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6235
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _5551, _5549, _5484
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_SET_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses', 'WormGearSetSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearSetSingleMeshWhineAnalysis',)


class WormGearSetSingleMeshWhineAnalysis(_5484.GearSetSingleMeshWhineAnalysis):
    '''WormGearSetSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_SET_SINGLE_MESH_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearSetSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2112.WormGearSet':
        '''WormGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2112.WormGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6235.WormGearSetLoadCase':
        '''WormGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6235.WormGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def worm_gears_single_mesh_whine_analysis(self) -> 'List[_5551.WormGearSingleMeshWhineAnalysis]':
        '''List[WormGearSingleMeshWhineAnalysis]: 'WormGearsSingleMeshWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearsSingleMeshWhineAnalysis, constructor.new(_5551.WormGearSingleMeshWhineAnalysis))
        return value

    @property
    def worm_meshes_single_mesh_whine_analysis(self) -> 'List[_5549.WormGearMeshSingleMeshWhineAnalysis]':
        '''List[WormGearMeshSingleMeshWhineAnalysis]: 'WormMeshesSingleMeshWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormMeshesSingleMeshWhineAnalysis, constructor.new(_5549.WormGearMeshSingleMeshWhineAnalysis))
        return value
