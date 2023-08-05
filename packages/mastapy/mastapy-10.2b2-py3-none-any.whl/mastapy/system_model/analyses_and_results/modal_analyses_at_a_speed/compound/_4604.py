'''_4604.py

AssemblyCompoundModalAnalysisAtASpeed
'''


from typing import List

from mastapy.system_model.part_model import _1999
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _4482
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
    _4605, _4607, _4610, _4616,
    _4617, _4618, _4623, _4628,
    _4638, _4642, _4648, _4649,
    _4656, _4657, _4664, _4667,
    _4668, _4669, _4671, _4673,
    _4678, _4679, _4680, _4687,
    _4682, _4686, _4692, _4693,
    _4698, _4701, _4704, _4708,
    _4712, _4716, _4719, _4599
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed.Compound', 'AssemblyCompoundModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyCompoundModalAnalysisAtASpeed',)


class AssemblyCompoundModalAnalysisAtASpeed(_4599.AbstractAssemblyCompoundModalAnalysisAtASpeed):
    '''AssemblyCompoundModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyCompoundModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_1999.Assembly':
        '''Assembly: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1999.Assembly)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_1999.Assembly':
        '''Assembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1999.Assembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4482.AssemblyModalAnalysisAtASpeed]':
        '''List[AssemblyModalAnalysisAtASpeed]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4482.AssemblyModalAnalysisAtASpeed))
        return value

    @property
    def assembly_modal_analysis_at_a_speed_load_cases(self) -> 'List[_4482.AssemblyModalAnalysisAtASpeed]':
        '''List[AssemblyModalAnalysisAtASpeed]: 'AssemblyModalAnalysisAtASpeedLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyModalAnalysisAtASpeedLoadCases, constructor.new(_4482.AssemblyModalAnalysisAtASpeed))
        return value

    @property
    def bearings(self) -> 'List[_4605.BearingCompoundModalAnalysisAtASpeed]':
        '''List[BearingCompoundModalAnalysisAtASpeed]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_4605.BearingCompoundModalAnalysisAtASpeed))
        return value

    @property
    def belt_drives(self) -> 'List[_4607.BeltDriveCompoundModalAnalysisAtASpeed]':
        '''List[BeltDriveCompoundModalAnalysisAtASpeed]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_4607.BeltDriveCompoundModalAnalysisAtASpeed))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_4610.BevelDifferentialGearSetCompoundModalAnalysisAtASpeed]':
        '''List[BevelDifferentialGearSetCompoundModalAnalysisAtASpeed]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_4610.BevelDifferentialGearSetCompoundModalAnalysisAtASpeed))
        return value

    @property
    def bolts(self) -> 'List[_4616.BoltCompoundModalAnalysisAtASpeed]':
        '''List[BoltCompoundModalAnalysisAtASpeed]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_4616.BoltCompoundModalAnalysisAtASpeed))
        return value

    @property
    def bolted_joints(self) -> 'List[_4617.BoltedJointCompoundModalAnalysisAtASpeed]':
        '''List[BoltedJointCompoundModalAnalysisAtASpeed]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_4617.BoltedJointCompoundModalAnalysisAtASpeed))
        return value

    @property
    def clutches(self) -> 'List[_4618.ClutchCompoundModalAnalysisAtASpeed]':
        '''List[ClutchCompoundModalAnalysisAtASpeed]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_4618.ClutchCompoundModalAnalysisAtASpeed))
        return value

    @property
    def concept_couplings(self) -> 'List[_4623.ConceptCouplingCompoundModalAnalysisAtASpeed]':
        '''List[ConceptCouplingCompoundModalAnalysisAtASpeed]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_4623.ConceptCouplingCompoundModalAnalysisAtASpeed))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_4628.ConceptGearSetCompoundModalAnalysisAtASpeed]':
        '''List[ConceptGearSetCompoundModalAnalysisAtASpeed]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_4628.ConceptGearSetCompoundModalAnalysisAtASpeed))
        return value

    @property
    def cv_ts(self) -> 'List[_4638.CVTCompoundModalAnalysisAtASpeed]':
        '''List[CVTCompoundModalAnalysisAtASpeed]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_4638.CVTCompoundModalAnalysisAtASpeed))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_4642.CylindricalGearSetCompoundModalAnalysisAtASpeed]':
        '''List[CylindricalGearSetCompoundModalAnalysisAtASpeed]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_4642.CylindricalGearSetCompoundModalAnalysisAtASpeed))
        return value

    @property
    def face_gear_sets(self) -> 'List[_4648.FaceGearSetCompoundModalAnalysisAtASpeed]':
        '''List[FaceGearSetCompoundModalAnalysisAtASpeed]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_4648.FaceGearSetCompoundModalAnalysisAtASpeed))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_4649.FlexiblePinAssemblyCompoundModalAnalysisAtASpeed]':
        '''List[FlexiblePinAssemblyCompoundModalAnalysisAtASpeed]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_4649.FlexiblePinAssemblyCompoundModalAnalysisAtASpeed))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_4656.HypoidGearSetCompoundModalAnalysisAtASpeed]':
        '''List[HypoidGearSetCompoundModalAnalysisAtASpeed]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_4656.HypoidGearSetCompoundModalAnalysisAtASpeed))
        return value

    @property
    def imported_fe_components(self) -> 'List[_4657.ImportedFEComponentCompoundModalAnalysisAtASpeed]':
        '''List[ImportedFEComponentCompoundModalAnalysisAtASpeed]: 'ImportedFEComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ImportedFEComponents, constructor.new(_4657.ImportedFEComponentCompoundModalAnalysisAtASpeed))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_4664.KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysisAtASpeed]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysisAtASpeed]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_4664.KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysisAtASpeed))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_4667.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysisAtASpeed]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysisAtASpeed]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_4667.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysisAtASpeed))
        return value

    @property
    def mass_discs(self) -> 'List[_4668.MassDiscCompoundModalAnalysisAtASpeed]':
        '''List[MassDiscCompoundModalAnalysisAtASpeed]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_4668.MassDiscCompoundModalAnalysisAtASpeed))
        return value

    @property
    def measurement_components(self) -> 'List[_4669.MeasurementComponentCompoundModalAnalysisAtASpeed]':
        '''List[MeasurementComponentCompoundModalAnalysisAtASpeed]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_4669.MeasurementComponentCompoundModalAnalysisAtASpeed))
        return value

    @property
    def oil_seals(self) -> 'List[_4671.OilSealCompoundModalAnalysisAtASpeed]':
        '''List[OilSealCompoundModalAnalysisAtASpeed]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_4671.OilSealCompoundModalAnalysisAtASpeed))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_4673.PartToPartShearCouplingCompoundModalAnalysisAtASpeed]':
        '''List[PartToPartShearCouplingCompoundModalAnalysisAtASpeed]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_4673.PartToPartShearCouplingCompoundModalAnalysisAtASpeed))
        return value

    @property
    def planet_carriers(self) -> 'List[_4678.PlanetCarrierCompoundModalAnalysisAtASpeed]':
        '''List[PlanetCarrierCompoundModalAnalysisAtASpeed]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_4678.PlanetCarrierCompoundModalAnalysisAtASpeed))
        return value

    @property
    def point_loads(self) -> 'List[_4679.PointLoadCompoundModalAnalysisAtASpeed]':
        '''List[PointLoadCompoundModalAnalysisAtASpeed]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_4679.PointLoadCompoundModalAnalysisAtASpeed))
        return value

    @property
    def power_loads(self) -> 'List[_4680.PowerLoadCompoundModalAnalysisAtASpeed]':
        '''List[PowerLoadCompoundModalAnalysisAtASpeed]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_4680.PowerLoadCompoundModalAnalysisAtASpeed))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_4687.ShaftHubConnectionCompoundModalAnalysisAtASpeed]':
        '''List[ShaftHubConnectionCompoundModalAnalysisAtASpeed]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_4687.ShaftHubConnectionCompoundModalAnalysisAtASpeed))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_4682.RollingRingAssemblyCompoundModalAnalysisAtASpeed]':
        '''List[RollingRingAssemblyCompoundModalAnalysisAtASpeed]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_4682.RollingRingAssemblyCompoundModalAnalysisAtASpeed))
        return value

    @property
    def shafts(self) -> 'List[_4686.ShaftCompoundModalAnalysisAtASpeed]':
        '''List[ShaftCompoundModalAnalysisAtASpeed]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_4686.ShaftCompoundModalAnalysisAtASpeed))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_4692.SpiralBevelGearSetCompoundModalAnalysisAtASpeed]':
        '''List[SpiralBevelGearSetCompoundModalAnalysisAtASpeed]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_4692.SpiralBevelGearSetCompoundModalAnalysisAtASpeed))
        return value

    @property
    def spring_dampers(self) -> 'List[_4693.SpringDamperCompoundModalAnalysisAtASpeed]':
        '''List[SpringDamperCompoundModalAnalysisAtASpeed]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_4693.SpringDamperCompoundModalAnalysisAtASpeed))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_4698.StraightBevelDiffGearSetCompoundModalAnalysisAtASpeed]':
        '''List[StraightBevelDiffGearSetCompoundModalAnalysisAtASpeed]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_4698.StraightBevelDiffGearSetCompoundModalAnalysisAtASpeed))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_4701.StraightBevelGearSetCompoundModalAnalysisAtASpeed]':
        '''List[StraightBevelGearSetCompoundModalAnalysisAtASpeed]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_4701.StraightBevelGearSetCompoundModalAnalysisAtASpeed))
        return value

    @property
    def synchronisers(self) -> 'List[_4704.SynchroniserCompoundModalAnalysisAtASpeed]':
        '''List[SynchroniserCompoundModalAnalysisAtASpeed]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_4704.SynchroniserCompoundModalAnalysisAtASpeed))
        return value

    @property
    def torque_converters(self) -> 'List[_4708.TorqueConverterCompoundModalAnalysisAtASpeed]':
        '''List[TorqueConverterCompoundModalAnalysisAtASpeed]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_4708.TorqueConverterCompoundModalAnalysisAtASpeed))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_4712.UnbalancedMassCompoundModalAnalysisAtASpeed]':
        '''List[UnbalancedMassCompoundModalAnalysisAtASpeed]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_4712.UnbalancedMassCompoundModalAnalysisAtASpeed))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_4716.WormGearSetCompoundModalAnalysisAtASpeed]':
        '''List[WormGearSetCompoundModalAnalysisAtASpeed]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_4716.WormGearSetCompoundModalAnalysisAtASpeed))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_4719.ZerolBevelGearSetCompoundModalAnalysisAtASpeed]':
        '''List[ZerolBevelGearSetCompoundModalAnalysisAtASpeed]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_4719.ZerolBevelGearSetCompoundModalAnalysisAtASpeed))
        return value
