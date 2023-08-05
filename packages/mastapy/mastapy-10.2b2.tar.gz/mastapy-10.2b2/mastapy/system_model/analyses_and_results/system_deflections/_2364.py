'''_2364.py

WormGearSystemDeflection
'''


from mastapy.system_model.part_model.gears import _2111
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6233
from mastapy.system_model.analyses_and_results.power_flows import _3358
from mastapy.gears.rating.worm import _176
from mastapy.system_model.analyses_and_results.system_deflections import _2291
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'WormGearSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearSystemDeflection',)


class WormGearSystemDeflection(_2291.GearSystemDeflection):
    '''WormGearSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2111.WormGear':
        '''WormGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2111.WormGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6233.WormGearLoadCase':
        '''WormGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6233.WormGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def power_flow_results(self) -> '_3358.WormGearPowerFlow':
        '''WormGearPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3358.WormGearPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def component_detailed_analysis(self) -> '_176.WormGearRating':
        '''WormGearRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_176.WormGearRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None
