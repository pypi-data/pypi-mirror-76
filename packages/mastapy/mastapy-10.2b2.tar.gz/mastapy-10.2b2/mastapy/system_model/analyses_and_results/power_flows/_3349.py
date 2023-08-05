'''_3349.py

SynchroniserSleevePowerFlow
'''


from mastapy.system_model.part_model.couplings import _2160
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6220
from mastapy.system_model.analyses_and_results.power_flows import _3347
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_SLEEVE_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'SynchroniserSleevePowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserSleevePowerFlow',)


class SynchroniserSleevePowerFlow(_3347.SynchroniserPartPowerFlow):
    '''SynchroniserSleevePowerFlow

    This is a mastapy class.
    '''

    TYPE = _SYNCHRONISER_SLEEVE_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SynchroniserSleevePowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2160.SynchroniserSleeve':
        '''SynchroniserSleeve: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2160.SynchroniserSleeve)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6220.SynchroniserSleeveLoadCase':
        '''SynchroniserSleeveLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6220.SynchroniserSleeveLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
