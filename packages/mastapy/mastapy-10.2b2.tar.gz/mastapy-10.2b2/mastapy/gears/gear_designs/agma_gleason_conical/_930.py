'''_930.py

AGMAGleasonConicalGearDesign
'''


from mastapy.gears.gear_designs.conical import (
    _901, _895, _894, _890,
    _900, _891
)
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy._internal.implicit import enum_with_selected_value
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal.python_net import python_net_import
from mastapy.gears.manufacturing.bevel.cutters import (
    _598, _599, _600, _601
)
from mastapy._internal.cast_exception import CastException
from mastapy.gears import _116
from mastapy.gears.gear_designs.cylindrical.accuracy_and_tolerances import _874, _878, _882
from mastapy.gears.gear_designs.agma_gleason_conical import _929
from mastapy.gears.materials import (
    _379, _368, _370, _372,
    _376, _382, _386, _388
)

_DATABASE_WITH_SELECTED_ITEM = python_net_import('SMT.MastaAPI.UtilityGUI.Databases', 'DatabaseWithSelectedItem')
_AGMA_GLEASON_CONICAL_GEAR_DESIGN = python_net_import('SMT.MastaAPI.Gears.GearDesigns.AGMAGleasonConical', 'AGMAGleasonConicalGearDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('AGMAGleasonConicalGearDesign',)


class AGMAGleasonConicalGearDesign(_891.ConicalGearDesign):
    '''AGMAGleasonConicalGearDesign

    This is a mastapy class.
    '''

    TYPE = _AGMA_GLEASON_CONICAL_GEAR_DESIGN

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AGMAGleasonConicalGearDesign.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def front_end_type(self) -> '_901.FrontEndTypes':
        '''FrontEndTypes: 'FrontEndType' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.FrontEndType)
        return constructor.new(_901.FrontEndTypes)(value) if value else None

    @front_end_type.setter
    def front_end_type(self, value: '_901.FrontEndTypes'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.FrontEndType = value

    @property
    def manufacture_method(self) -> 'enum_with_selected_value.EnumWithSelectedValue_ConicalManufactureMethods':
        '''enum_with_selected_value.EnumWithSelectedValue_ConicalManufactureMethods: 'ManufactureMethod' is the original name of this property.'''

        value = enum_with_selected_value.EnumWithSelectedValue_ConicalManufactureMethods.wrapped_type()
        return enum_with_selected_value_runtime.create(self.wrapped.ManufactureMethod, value) if self.wrapped.ManufactureMethod else None

    @manufacture_method.setter
    def manufacture_method(self, value: 'enum_with_selected_value.EnumWithSelectedValue_ConicalManufactureMethods.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ConicalManufactureMethods.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.ManufactureMethod = value

    @property
    def machine_setting_calculation_method(self) -> 'enum_with_selected_value.EnumWithSelectedValue_ConicalMachineSettingCalculationMethods':
        '''enum_with_selected_value.EnumWithSelectedValue_ConicalMachineSettingCalculationMethods: 'MachineSettingCalculationMethod' is the original name of this property.'''

        value = enum_with_selected_value.EnumWithSelectedValue_ConicalMachineSettingCalculationMethods.wrapped_type()
        return enum_with_selected_value_runtime.create(self.wrapped.MachineSettingCalculationMethod, value) if self.wrapped.MachineSettingCalculationMethod else None

    @machine_setting_calculation_method.setter
    def machine_setting_calculation_method(self, value: 'enum_with_selected_value.EnumWithSelectedValue_ConicalMachineSettingCalculationMethods.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ConicalMachineSettingCalculationMethods.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.MachineSettingCalculationMethod = value

    @property
    def material(self) -> 'str':
        '''str: 'Material' is the original name of this property.'''

        return self.wrapped.Material.SelectedItemName

    @material.setter
    def material(self, value: 'str'):
        self.wrapped.Material.SetSelectedItem(str(value) if value else None)

    @property
    def allowable_bending_stress(self) -> 'float':
        '''float: 'AllowableBendingStress' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AllowableBendingStress

    @property
    def allowable_contact_stress(self) -> 'float':
        '''float: 'AllowableContactStress' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AllowableContactStress

    @property
    def face_width(self) -> 'float':
        '''float: 'FaceWidth' is the original name of this property.'''

        return self.wrapped.FaceWidth

    @face_width.setter
    def face_width(self, value: 'float'):
        self.wrapped.FaceWidth = float(value) if value else 0.0

    @property
    def cutter(self) -> '_890.ConicalGearCutter':
        '''ConicalGearCutter: 'Cutter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_890.ConicalGearCutter)(self.wrapped.Cutter) if self.wrapped.Cutter else None

    @property
    def cutter_of_type_pinion_finish_cutter(self) -> '_598.PinionFinishCutter':
        '''PinionFinishCutter: 'Cutter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _598.PinionFinishCutter.TYPE not in self.wrapped.Cutter.__class__.__mro__:
            raise CastException('Failed to cast cutter to PinionFinishCutter. Expected: {}.'.format(self.wrapped.Cutter.__class__.__qualname__))

        return constructor.new(_598.PinionFinishCutter)(self.wrapped.Cutter) if self.wrapped.Cutter else None

    @property
    def cutter_of_type_pinion_rough_cutter(self) -> '_599.PinionRoughCutter':
        '''PinionRoughCutter: 'Cutter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _599.PinionRoughCutter.TYPE not in self.wrapped.Cutter.__class__.__mro__:
            raise CastException('Failed to cast cutter to PinionRoughCutter. Expected: {}.'.format(self.wrapped.Cutter.__class__.__qualname__))

        return constructor.new(_599.PinionRoughCutter)(self.wrapped.Cutter) if self.wrapped.Cutter else None

    @property
    def cutter_of_type_wheel_finish_cutter(self) -> '_600.WheelFinishCutter':
        '''WheelFinishCutter: 'Cutter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _600.WheelFinishCutter.TYPE not in self.wrapped.Cutter.__class__.__mro__:
            raise CastException('Failed to cast cutter to WheelFinishCutter. Expected: {}.'.format(self.wrapped.Cutter.__class__.__qualname__))

        return constructor.new(_600.WheelFinishCutter)(self.wrapped.Cutter) if self.wrapped.Cutter else None

    @property
    def cutter_of_type_wheel_rough_cutter(self) -> '_601.WheelRoughCutter':
        '''WheelRoughCutter: 'Cutter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _601.WheelRoughCutter.TYPE not in self.wrapped.Cutter.__class__.__mro__:
            raise CastException('Failed to cast cutter to WheelRoughCutter. Expected: {}.'.format(self.wrapped.Cutter.__class__.__qualname__))

        return constructor.new(_601.WheelRoughCutter)(self.wrapped.Cutter) if self.wrapped.Cutter else None

    @property
    def cutter_of_type_dummy_conical_gear_cutter(self) -> '_900.DummyConicalGearCutter':
        '''DummyConicalGearCutter: 'Cutter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _900.DummyConicalGearCutter.TYPE not in self.wrapped.Cutter.__class__.__mro__:
            raise CastException('Failed to cast cutter to DummyConicalGearCutter. Expected: {}.'.format(self.wrapped.Cutter.__class__.__qualname__))

        return constructor.new(_900.DummyConicalGearCutter)(self.wrapped.Cutter) if self.wrapped.Cutter else None

    @property
    def accuracy_grades(self) -> '_116.AccuracyGrades':
        '''AccuracyGrades: 'AccuracyGrades' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_116.AccuracyGrades)(self.wrapped.AccuracyGrades) if self.wrapped.AccuracyGrades else None

    @property
    def accuracy_grades_of_type_agma20151_accuracy_grades(self) -> '_874.AGMA20151AccuracyGrades':
        '''AGMA20151AccuracyGrades: 'AccuracyGrades' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _874.AGMA20151AccuracyGrades.TYPE not in self.wrapped.AccuracyGrades.__class__.__mro__:
            raise CastException('Failed to cast accuracy_grades to AGMA20151AccuracyGrades. Expected: {}.'.format(self.wrapped.AccuracyGrades.__class__.__qualname__))

        return constructor.new(_874.AGMA20151AccuracyGrades)(self.wrapped.AccuracyGrades) if self.wrapped.AccuracyGrades else None

    @property
    def accuracy_grades_of_type_cylindrical_accuracy_grades(self) -> '_878.CylindricalAccuracyGrades':
        '''CylindricalAccuracyGrades: 'AccuracyGrades' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _878.CylindricalAccuracyGrades.TYPE not in self.wrapped.AccuracyGrades.__class__.__mro__:
            raise CastException('Failed to cast accuracy_grades to CylindricalAccuracyGrades. Expected: {}.'.format(self.wrapped.AccuracyGrades.__class__.__qualname__))

        return constructor.new(_878.CylindricalAccuracyGrades)(self.wrapped.AccuracyGrades) if self.wrapped.AccuracyGrades else None

    @property
    def accuracy_grades_of_type_iso1328_accuracy_grades(self) -> '_882.ISO1328AccuracyGrades':
        '''ISO1328AccuracyGrades: 'AccuracyGrades' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _882.ISO1328AccuracyGrades.TYPE not in self.wrapped.AccuracyGrades.__class__.__mro__:
            raise CastException('Failed to cast accuracy_grades to ISO1328AccuracyGrades. Expected: {}.'.format(self.wrapped.AccuracyGrades.__class__.__qualname__))

        return constructor.new(_882.ISO1328AccuracyGrades)(self.wrapped.AccuracyGrades) if self.wrapped.AccuracyGrades else None

    @property
    def accuracy_grades_of_type_agma_gleason_conical_accuracy_grades(self) -> '_929.AGMAGleasonConicalAccuracyGrades':
        '''AGMAGleasonConicalAccuracyGrades: 'AccuracyGrades' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _929.AGMAGleasonConicalAccuracyGrades.TYPE not in self.wrapped.AccuracyGrades.__class__.__mro__:
            raise CastException('Failed to cast accuracy_grades to AGMAGleasonConicalAccuracyGrades. Expected: {}.'.format(self.wrapped.AccuracyGrades.__class__.__qualname__))

        return constructor.new(_929.AGMAGleasonConicalAccuracyGrades)(self.wrapped.AccuracyGrades) if self.wrapped.AccuracyGrades else None

    @property
    def bevel_gear_material(self) -> '_379.GearMaterial':
        '''GearMaterial: 'BevelGearMaterial' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_379.GearMaterial)(self.wrapped.BevelGearMaterial) if self.wrapped.BevelGearMaterial else None

    @property
    def bevel_gear_material_of_type_agma_cylindrical_gear_material(self) -> '_368.AGMACylindricalGearMaterial':
        '''AGMACylindricalGearMaterial: 'BevelGearMaterial' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _368.AGMACylindricalGearMaterial.TYPE not in self.wrapped.BevelGearMaterial.__class__.__mro__:
            raise CastException('Failed to cast bevel_gear_material to AGMACylindricalGearMaterial. Expected: {}.'.format(self.wrapped.BevelGearMaterial.__class__.__qualname__))

        return constructor.new(_368.AGMACylindricalGearMaterial)(self.wrapped.BevelGearMaterial) if self.wrapped.BevelGearMaterial else None

    @property
    def bevel_gear_material_of_type_bevel_gear_iso_material(self) -> '_370.BevelGearISOMaterial':
        '''BevelGearISOMaterial: 'BevelGearMaterial' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _370.BevelGearISOMaterial.TYPE not in self.wrapped.BevelGearMaterial.__class__.__mro__:
            raise CastException('Failed to cast bevel_gear_material to BevelGearISOMaterial. Expected: {}.'.format(self.wrapped.BevelGearMaterial.__class__.__qualname__))

        return constructor.new(_370.BevelGearISOMaterial)(self.wrapped.BevelGearMaterial) if self.wrapped.BevelGearMaterial else None

    @property
    def bevel_gear_material_of_type_bevel_gear_material(self) -> '_372.BevelGearMaterial':
        '''BevelGearMaterial: 'BevelGearMaterial' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _372.BevelGearMaterial.TYPE not in self.wrapped.BevelGearMaterial.__class__.__mro__:
            raise CastException('Failed to cast bevel_gear_material to BevelGearMaterial. Expected: {}.'.format(self.wrapped.BevelGearMaterial.__class__.__qualname__))

        return constructor.new(_372.BevelGearMaterial)(self.wrapped.BevelGearMaterial) if self.wrapped.BevelGearMaterial else None

    @property
    def bevel_gear_material_of_type_cylindrical_gear_material(self) -> '_376.CylindricalGearMaterial':
        '''CylindricalGearMaterial: 'BevelGearMaterial' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _376.CylindricalGearMaterial.TYPE not in self.wrapped.BevelGearMaterial.__class__.__mro__:
            raise CastException('Failed to cast bevel_gear_material to CylindricalGearMaterial. Expected: {}.'.format(self.wrapped.BevelGearMaterial.__class__.__qualname__))

        return constructor.new(_376.CylindricalGearMaterial)(self.wrapped.BevelGearMaterial) if self.wrapped.BevelGearMaterial else None

    @property
    def bevel_gear_material_of_type_iso_cylindrical_gear_material(self) -> '_382.ISOCylindricalGearMaterial':
        '''ISOCylindricalGearMaterial: 'BevelGearMaterial' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _382.ISOCylindricalGearMaterial.TYPE not in self.wrapped.BevelGearMaterial.__class__.__mro__:
            raise CastException('Failed to cast bevel_gear_material to ISOCylindricalGearMaterial. Expected: {}.'.format(self.wrapped.BevelGearMaterial.__class__.__qualname__))

        return constructor.new(_382.ISOCylindricalGearMaterial)(self.wrapped.BevelGearMaterial) if self.wrapped.BevelGearMaterial else None

    @property
    def bevel_gear_material_of_type_klingelnberg_cyclo_palloid_conical_gear_material(self) -> '_386.KlingelnbergCycloPalloidConicalGearMaterial':
        '''KlingelnbergCycloPalloidConicalGearMaterial: 'BevelGearMaterial' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _386.KlingelnbergCycloPalloidConicalGearMaterial.TYPE not in self.wrapped.BevelGearMaterial.__class__.__mro__:
            raise CastException('Failed to cast bevel_gear_material to KlingelnbergCycloPalloidConicalGearMaterial. Expected: {}.'.format(self.wrapped.BevelGearMaterial.__class__.__qualname__))

        return constructor.new(_386.KlingelnbergCycloPalloidConicalGearMaterial)(self.wrapped.BevelGearMaterial) if self.wrapped.BevelGearMaterial else None

    @property
    def bevel_gear_material_of_type_plastic_cylindrical_gear_material(self) -> '_388.PlasticCylindricalGearMaterial':
        '''PlasticCylindricalGearMaterial: 'BevelGearMaterial' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _388.PlasticCylindricalGearMaterial.TYPE not in self.wrapped.BevelGearMaterial.__class__.__mro__:
            raise CastException('Failed to cast bevel_gear_material to PlasticCylindricalGearMaterial. Expected: {}.'.format(self.wrapped.BevelGearMaterial.__class__.__qualname__))

        return constructor.new(_388.PlasticCylindricalGearMaterial)(self.wrapped.BevelGearMaterial) if self.wrapped.BevelGearMaterial else None
