'''_5472.py

CVTSingleMeshWhineAnalysis
'''


from mastapy.system_model.part_model.couplings import _2141
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _5440
from mastapy._internal.python_net import python_net_import

_CVT_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses', 'CVTSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTSingleMeshWhineAnalysis',)


class CVTSingleMeshWhineAnalysis(_5440.BeltDriveSingleMeshWhineAnalysis):
    '''CVTSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _CVT_SINGLE_MESH_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2141.CVT':
        '''CVT: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2141.CVT)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None
