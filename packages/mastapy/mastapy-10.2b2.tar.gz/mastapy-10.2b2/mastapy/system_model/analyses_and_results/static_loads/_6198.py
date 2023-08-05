'''_6198.py

ShaftLoadCase
'''


from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import constructor
from mastapy.system_model.part_model.shaft_model import _2043
from mastapy.system_model.analyses_and_results.static_loads import _6071
from mastapy._internal.python_net import python_net_import

_SHAFT_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'ShaftLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftLoadCase',)


class ShaftLoadCase(_6071.AbstractShaftOrHousingLoadCase):
    '''ShaftLoadCase

    This is a mastapy class.
    '''

    TYPE = _SHAFT_LOAD_CASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftLoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def shaft_temperature(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'ShaftTemperature' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.ShaftTemperature) if self.wrapped.ShaftTemperature else None

    @shaft_temperature.setter
    def shaft_temperature(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.ShaftTemperature = value

    @property
    def diameter_scaling_factor(self) -> 'float':
        '''float: 'DiameterScalingFactor' is the original name of this property.'''

        return self.wrapped.DiameterScalingFactor

    @diameter_scaling_factor.setter
    def diameter_scaling_factor(self, value: 'float'):
        self.wrapped.DiameterScalingFactor = float(value) if value else 0.0

    @property
    def component_design(self) -> '_2043.Shaft':
        '''Shaft: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2043.Shaft)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None
