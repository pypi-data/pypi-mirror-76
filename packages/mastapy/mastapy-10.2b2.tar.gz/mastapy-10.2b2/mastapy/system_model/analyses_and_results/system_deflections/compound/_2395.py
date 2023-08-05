'''_2395.py

BoltedJointCompoundSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model import _2007
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections import _2246
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2468
from mastapy._internal.python_net import python_net_import

_BOLTED_JOINT_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'BoltedJointCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('BoltedJointCompoundSystemDeflection',)


class BoltedJointCompoundSystemDeflection(_2468.SpecialisedAssemblyCompoundSystemDeflection):
    '''BoltedJointCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _BOLTED_JOINT_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BoltedJointCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2007.BoltedJoint':
        '''BoltedJoint: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2007.BoltedJoint)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2007.BoltedJoint':
        '''BoltedJoint: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2007.BoltedJoint)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_2246.BoltedJointSystemDeflection]':
        '''List[BoltedJointSystemDeflection]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_2246.BoltedJointSystemDeflection))
        return value

    @property
    def assembly_system_deflection_load_cases(self) -> 'List[_2246.BoltedJointSystemDeflection]':
        '''List[BoltedJointSystemDeflection]: 'AssemblySystemDeflectionLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySystemDeflectionLoadCases, constructor.new(_2246.BoltedJointSystemDeflection))
        return value
