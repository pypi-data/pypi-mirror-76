﻿'''_5907.py

RootAssemblyDynamicAnalysis
'''


from mastapy.system_model.part_model import _2036
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.dynamic_analyses import _5865, _5824
from mastapy._internal.python_net import python_net_import

_ROOT_ASSEMBLY_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'RootAssemblyDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('RootAssemblyDynamicAnalysis',)


class RootAssemblyDynamicAnalysis(_5824.AssemblyDynamicAnalysis):
    '''RootAssemblyDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _ROOT_ASSEMBLY_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RootAssemblyDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2036.RootAssembly':
        '''RootAssembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2036.RootAssembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def dynamic_analysis_inputs(self) -> '_5865.DynamicAnalysis':
        '''DynamicAnalysis: 'DynamicAnalysisInputs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5865.DynamicAnalysis)(self.wrapped.DynamicAnalysisInputs) if self.wrapped.DynamicAnalysisInputs else None
