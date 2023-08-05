﻿'''_3569.py

ParametricStudyTool
'''


from mastapy.system_model.analyses_and_results.parametric_study_tools import _3570
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6222, _6208
from mastapy.system_model.analyses_and_results.analysis_cases import _6506
from mastapy._internal.python_net import python_net_import

_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'ParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('ParametricStudyTool',)


class ParametricStudyTool(_6506.AnalysisCase):
    '''ParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def parametric_analysis_options(self) -> '_3570.ParametricStudyToolOptions':
        '''ParametricStudyToolOptions: 'ParametricAnalysisOptions' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3570.ParametricStudyToolOptions)(self.wrapped.ParametricAnalysisOptions) if self.wrapped.ParametricAnalysisOptions else None

    @property
    def time_series_load_case(self) -> '_6222.TimeSeriesLoadCase':
        '''TimeSeriesLoadCase: 'TimeSeriesLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6222.TimeSeriesLoadCase)(self.wrapped.TimeSeriesLoadCase) if self.wrapped.TimeSeriesLoadCase else None

    @property
    def load_case(self) -> '_6208.StaticLoadCase':
        '''StaticLoadCase: 'LoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6208.StaticLoadCase)(self.wrapped.LoadCase) if self.wrapped.LoadCase else None
