﻿'''_4155.py

CylindricalGearSetCompoundModalAnalysesAtSpeeds
'''


from typing import List

from mastapy.system_model.part_model.gears import _2086
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns.compound import _4153, _4154, _4165
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns import _4030
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_SET_COMPOUND_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS.Compound', 'CylindricalGearSetCompoundModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearSetCompoundModalAnalysesAtSpeeds',)


class CylindricalGearSetCompoundModalAnalysesAtSpeeds(_4165.GearSetCompoundModalAnalysesAtSpeeds):
    '''CylindricalGearSetCompoundModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_SET_COMPOUND_MODAL_ANALYSES_AT_SPEEDS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearSetCompoundModalAnalysesAtSpeeds.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2086.CylindricalGearSet':
        '''CylindricalGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2086.CylindricalGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2086.CylindricalGearSet':
        '''CylindricalGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2086.CylindricalGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def cylindrical_gears_compound_modal_analyses_at_speeds(self) -> 'List[_4153.CylindricalGearCompoundModalAnalysesAtSpeeds]':
        '''List[CylindricalGearCompoundModalAnalysesAtSpeeds]: 'CylindricalGearsCompoundModalAnalysesAtSpeeds' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearsCompoundModalAnalysesAtSpeeds, constructor.new(_4153.CylindricalGearCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def cylindrical_meshes_compound_modal_analyses_at_speeds(self) -> 'List[_4154.CylindricalGearMeshCompoundModalAnalysesAtSpeeds]':
        '''List[CylindricalGearMeshCompoundModalAnalysesAtSpeeds]: 'CylindricalMeshesCompoundModalAnalysesAtSpeeds' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalMeshesCompoundModalAnalysesAtSpeeds, constructor.new(_4154.CylindricalGearMeshCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_4030.CylindricalGearSetModalAnalysesAtSpeeds]':
        '''List[CylindricalGearSetModalAnalysesAtSpeeds]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4030.CylindricalGearSetModalAnalysesAtSpeeds))
        return value

    @property
    def assembly_modal_analyses_at_speeds_load_cases(self) -> 'List[_4030.CylindricalGearSetModalAnalysesAtSpeeds]':
        '''List[CylindricalGearSetModalAnalysesAtSpeeds]: 'AssemblyModalAnalysesAtSpeedsLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyModalAnalysesAtSpeedsLoadCases, constructor.new(_4030.CylindricalGearSetModalAnalysesAtSpeeds))
        return value
