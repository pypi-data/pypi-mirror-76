﻿'''_5515.py

PulleySingleMeshWhineAnalysis
'''


from mastapy.system_model.part_model.couplings import _2145
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6191
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _5468
from mastapy._internal.python_net import python_net_import

_PULLEY_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses', 'PulleySingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PulleySingleMeshWhineAnalysis',)


class PulleySingleMeshWhineAnalysis(_5468.CouplingHalfSingleMeshWhineAnalysis):
    '''PulleySingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _PULLEY_SINGLE_MESH_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PulleySingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2145.Pulley':
        '''Pulley: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2145.Pulley)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6191.PulleyLoadCase':
        '''PulleyLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6191.PulleyLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
