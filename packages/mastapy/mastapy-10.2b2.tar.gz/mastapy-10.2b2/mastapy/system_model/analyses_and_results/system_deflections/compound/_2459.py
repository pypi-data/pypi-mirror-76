﻿'''_2459.py

PulleyCompoundSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2145
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections import _2322
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2414
from mastapy._internal.python_net import python_net_import

_PULLEY_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'PulleyCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('PulleyCompoundSystemDeflection',)


class PulleyCompoundSystemDeflection(_2414.CouplingHalfCompoundSystemDeflection):
    '''PulleyCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _PULLEY_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PulleyCompoundSystemDeflection.TYPE'):
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
    def load_case_analyses_ready(self) -> 'List[_2322.PulleySystemDeflection]':
        '''List[PulleySystemDeflection]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_2322.PulleySystemDeflection))
        return value

    @property
    def component_system_deflection_load_cases(self) -> 'List[_2322.PulleySystemDeflection]':
        '''List[PulleySystemDeflection]: 'ComponentSystemDeflectionLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionLoadCases, constructor.new(_2322.PulleySystemDeflection))
        return value
