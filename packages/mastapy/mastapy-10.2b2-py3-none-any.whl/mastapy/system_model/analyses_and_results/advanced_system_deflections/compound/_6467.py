﻿'''_6467.py

PulleyCompoundAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2145
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _6344
from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import _6422
from mastapy._internal.python_net import python_net_import

_PULLEY_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound', 'PulleyCompoundAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('PulleyCompoundAdvancedSystemDeflection',)


class PulleyCompoundAdvancedSystemDeflection(_6422.CouplingHalfCompoundAdvancedSystemDeflection):
    '''PulleyCompoundAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _PULLEY_COMPOUND_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PulleyCompoundAdvancedSystemDeflection.TYPE'):
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
    def load_case_analyses_ready(self) -> 'List[_6344.PulleyAdvancedSystemDeflection]':
        '''List[PulleyAdvancedSystemDeflection]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_6344.PulleyAdvancedSystemDeflection))
        return value

    @property
    def component_advanced_system_deflection_load_cases(self) -> 'List[_6344.PulleyAdvancedSystemDeflection]':
        '''List[PulleyAdvancedSystemDeflection]: 'ComponentAdvancedSystemDeflectionLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAdvancedSystemDeflectionLoadCases, constructor.new(_6344.PulleyAdvancedSystemDeflection))
        return value
