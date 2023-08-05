'''_5449.py

BoltedJointSingleMeshWhineAnalysis
'''


from mastapy.system_model.part_model import _2007
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6089
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _5524
from mastapy._internal.python_net import python_net_import

_BOLTED_JOINT_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses', 'BoltedJointSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BoltedJointSingleMeshWhineAnalysis',)


class BoltedJointSingleMeshWhineAnalysis(_5524.SpecialisedAssemblySingleMeshWhineAnalysis):
    '''BoltedJointSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _BOLTED_JOINT_SINGLE_MESH_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BoltedJointSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2007.BoltedJoint':
        '''BoltedJoint: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2007.BoltedJoint)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6089.BoltedJointLoadCase':
        '''BoltedJointLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6089.BoltedJointLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None
