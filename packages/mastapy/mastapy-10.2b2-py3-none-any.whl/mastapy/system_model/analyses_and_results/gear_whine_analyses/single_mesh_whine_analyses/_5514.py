'''_5514.py

PowerLoadSingleMeshWhineAnalysis
'''


from mastapy.system_model.part_model import _2034
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6190
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _5548
from mastapy._internal.python_net import python_net_import

_POWER_LOAD_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses', 'PowerLoadSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PowerLoadSingleMeshWhineAnalysis',)


class PowerLoadSingleMeshWhineAnalysis(_5548.VirtualComponentSingleMeshWhineAnalysis):
    '''PowerLoadSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _POWER_LOAD_SINGLE_MESH_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PowerLoadSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2034.PowerLoad':
        '''PowerLoad: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2034.PowerLoad)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6190.PowerLoadLoadCase':
        '''PowerLoadLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6190.PowerLoadLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
