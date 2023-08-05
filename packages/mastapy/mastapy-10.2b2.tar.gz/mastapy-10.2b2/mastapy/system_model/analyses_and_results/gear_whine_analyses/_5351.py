'''_5351.py

HypoidGearGearWhineAnalysis
'''


from mastapy.system_model.part_model.gears import _2094
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6157
from mastapy.system_model.analyses_and_results.system_deflections import _2295
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5276
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'HypoidGearGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearGearWhineAnalysis',)


class HypoidGearGearWhineAnalysis(_5276.AGMAGleasonConicalGearGearWhineAnalysis):
    '''HypoidGearGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGearGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2094.HypoidGear':
        '''HypoidGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2094.HypoidGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6157.HypoidGearLoadCase':
        '''HypoidGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6157.HypoidGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def system_deflection_results(self) -> '_2295.HypoidGearSystemDeflection':
        '''HypoidGearSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2295.HypoidGearSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
