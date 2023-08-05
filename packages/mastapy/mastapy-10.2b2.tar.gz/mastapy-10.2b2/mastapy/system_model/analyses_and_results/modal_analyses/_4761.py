'''_4761.py

CVTPulleyModalAnalysis
'''


from mastapy.system_model.part_model.couplings import _2142
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.system_deflections import _2270
from mastapy.system_model.analyses_and_results.modal_analyses import _4809
from mastapy._internal.python_net import python_net_import

_CVT_PULLEY_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'CVTPulleyModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTPulleyModalAnalysis',)


class CVTPulleyModalAnalysis(_4809.PulleyModalAnalysis):
    '''CVTPulleyModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _CVT_PULLEY_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTPulleyModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2142.CVTPulley':
        '''CVTPulley: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2142.CVTPulley)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def system_deflection_results(self) -> '_2270.CVTPulleySystemDeflection':
        '''CVTPulleySystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2270.CVTPulleySystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
