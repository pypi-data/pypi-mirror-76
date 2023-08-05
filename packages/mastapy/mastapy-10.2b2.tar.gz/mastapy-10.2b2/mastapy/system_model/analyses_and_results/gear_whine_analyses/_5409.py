'''_5409.py

TorqueConverterGearWhineAnalysis
'''


from mastapy.system_model.part_model.couplings import _2161
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6224
from mastapy.system_model.analyses_and_results.system_deflections import _2356
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5311
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'TorqueConverterGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterGearWhineAnalysis',)


class TorqueConverterGearWhineAnalysis(_5311.CouplingGearWhineAnalysis):
    '''TorqueConverterGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2161.TorqueConverter':
        '''TorqueConverter: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2161.TorqueConverter)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6224.TorqueConverterLoadCase':
        '''TorqueConverterLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6224.TorqueConverterLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def system_deflection_results(self) -> '_2356.TorqueConverterSystemDeflection':
        '''TorqueConverterSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2356.TorqueConverterSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
