﻿'''_4594.py

WormGearModalAnalysisAtASpeed
'''


from mastapy.system_model.part_model.gears import _2111
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6233
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _4529
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed', 'WormGearModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearModalAnalysisAtASpeed',)


class WormGearModalAnalysisAtASpeed(_4529.GearModalAnalysisAtASpeed):
    '''WormGearModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_MODAL_ANALYSIS_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearModalAnalysisAtASpeed.TYPE'):
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
