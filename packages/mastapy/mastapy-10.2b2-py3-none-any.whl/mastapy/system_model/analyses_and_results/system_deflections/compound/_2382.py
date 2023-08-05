'''_2382.py

AssemblyCompoundSystemDeflection
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model import _1999
from mastapy.nodal_analysis import _1365
from mastapy.shafts import _37
from mastapy.gears.analysis import _961
from mastapy.system_model.analyses_and_results.system_deflections import _2234
from mastapy.system_model.analyses_and_results.system_deflections.compound import (
    _2383, _2385, _2388, _2394,
    _2395, _2396, _2401, _2406,
    _2416, _2420, _2426, _2427,
    _2434, _2435, _2442, _2445,
    _2446, _2447, _2449, _2451,
    _2456, _2457, _2458, _2466,
    _2460, _2464, _2471, _2472,
    _2477, _2480, _2483, _2487,
    _2491, _2495, _2498, _2377
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'AssemblyCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyCompoundSystemDeflection',)


class AssemblyCompoundSystemDeflection(_2377.AbstractAssemblyCompoundSystemDeflection):
    '''AssemblyCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def overall_duty_cycle_shaft_reliability(self) -> 'float':
        '''float: 'OverallDutyCycleShaftReliability' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.OverallDutyCycleShaftReliability

    @property
    def overall_duty_cycle_bearing_reliability(self) -> 'float':
        '''float: 'OverallDutyCycleBearingReliability' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.OverallDutyCycleBearingReliability

    @property
    def overall_duty_cycle_gear_reliability(self) -> 'float':
        '''float: 'OverallDutyCycleGearReliability' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.OverallDutyCycleGearReliability

    @property
    def overall_oil_seal_duty_cycle_reliability(self) -> 'float':
        '''float: 'OverallOilSealDutyCycleReliability' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.OverallOilSealDutyCycleReliability

    @property
    def overall_system_reliability(self) -> 'float':
        '''float: 'OverallSystemReliability' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.OverallSystemReliability

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
    def analysis_settings(self) -> '_1365.AnalysisSettings':
        '''AnalysisSettings: 'AnalysisSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1365.AnalysisSettings)(self.wrapped.AnalysisSettings) if self.wrapped.AnalysisSettings else None

    @property
    def shaft_settings(self) -> '_37.ShaftSettings':
        '''ShaftSettings: 'ShaftSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_37.ShaftSettings)(self.wrapped.ShaftSettings) if self.wrapped.ShaftSettings else None

    @property
    def rating_for_all_gear_sets(self) -> '_961.GearSetGroupDutyCycle':
        '''GearSetGroupDutyCycle: 'RatingForAllGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_961.GearSetGroupDutyCycle)(self.wrapped.RatingForAllGearSets) if self.wrapped.RatingForAllGearSets else None

    @property
    def load_case_analyses_ready(self) -> 'List[_2234.AssemblySystemDeflection]':
        '''List[AssemblySystemDeflection]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_2234.AssemblySystemDeflection))
        return value

    @property
    def assembly_system_deflection_load_cases(self) -> 'List[_2234.AssemblySystemDeflection]':
        '''List[AssemblySystemDeflection]: 'AssemblySystemDeflectionLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySystemDeflectionLoadCases, constructor.new(_2234.AssemblySystemDeflection))
        return value

    @property
    def bearings(self) -> 'List[_2383.BearingCompoundSystemDeflection]':
        '''List[BearingCompoundSystemDeflection]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_2383.BearingCompoundSystemDeflection))
        return value

    @property
    def belt_drives(self) -> 'List[_2385.BeltDriveCompoundSystemDeflection]':
        '''List[BeltDriveCompoundSystemDeflection]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_2385.BeltDriveCompoundSystemDeflection))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_2388.BevelDifferentialGearSetCompoundSystemDeflection]':
        '''List[BevelDifferentialGearSetCompoundSystemDeflection]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_2388.BevelDifferentialGearSetCompoundSystemDeflection))
        return value

    @property
    def bolts(self) -> 'List[_2394.BoltCompoundSystemDeflection]':
        '''List[BoltCompoundSystemDeflection]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_2394.BoltCompoundSystemDeflection))
        return value

    @property
    def bolted_joints(self) -> 'List[_2395.BoltedJointCompoundSystemDeflection]':
        '''List[BoltedJointCompoundSystemDeflection]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_2395.BoltedJointCompoundSystemDeflection))
        return value

    @property
    def clutches(self) -> 'List[_2396.ClutchCompoundSystemDeflection]':
        '''List[ClutchCompoundSystemDeflection]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_2396.ClutchCompoundSystemDeflection))
        return value

    @property
    def concept_couplings(self) -> 'List[_2401.ConceptCouplingCompoundSystemDeflection]':
        '''List[ConceptCouplingCompoundSystemDeflection]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_2401.ConceptCouplingCompoundSystemDeflection))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_2406.ConceptGearSetCompoundSystemDeflection]':
        '''List[ConceptGearSetCompoundSystemDeflection]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_2406.ConceptGearSetCompoundSystemDeflection))
        return value

    @property
    def cv_ts(self) -> 'List[_2416.CVTCompoundSystemDeflection]':
        '''List[CVTCompoundSystemDeflection]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_2416.CVTCompoundSystemDeflection))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_2420.CylindricalGearSetCompoundSystemDeflection]':
        '''List[CylindricalGearSetCompoundSystemDeflection]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_2420.CylindricalGearSetCompoundSystemDeflection))
        return value

    @property
    def face_gear_sets(self) -> 'List[_2426.FaceGearSetCompoundSystemDeflection]':
        '''List[FaceGearSetCompoundSystemDeflection]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_2426.FaceGearSetCompoundSystemDeflection))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_2427.FlexiblePinAssemblyCompoundSystemDeflection]':
        '''List[FlexiblePinAssemblyCompoundSystemDeflection]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_2427.FlexiblePinAssemblyCompoundSystemDeflection))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_2434.HypoidGearSetCompoundSystemDeflection]':
        '''List[HypoidGearSetCompoundSystemDeflection]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_2434.HypoidGearSetCompoundSystemDeflection))
        return value

    @property
    def imported_fe_components(self) -> 'List[_2435.ImportedFEComponentCompoundSystemDeflection]':
        '''List[ImportedFEComponentCompoundSystemDeflection]: 'ImportedFEComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ImportedFEComponents, constructor.new(_2435.ImportedFEComponentCompoundSystemDeflection))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_2442.KlingelnbergCycloPalloidHypoidGearSetCompoundSystemDeflection]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetCompoundSystemDeflection]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_2442.KlingelnbergCycloPalloidHypoidGearSetCompoundSystemDeflection))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_2445.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSystemDeflection]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSystemDeflection]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_2445.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSystemDeflection))
        return value

    @property
    def mass_discs(self) -> 'List[_2446.MassDiscCompoundSystemDeflection]':
        '''List[MassDiscCompoundSystemDeflection]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_2446.MassDiscCompoundSystemDeflection))
        return value

    @property
    def measurement_components(self) -> 'List[_2447.MeasurementComponentCompoundSystemDeflection]':
        '''List[MeasurementComponentCompoundSystemDeflection]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_2447.MeasurementComponentCompoundSystemDeflection))
        return value

    @property
    def oil_seals(self) -> 'List[_2449.OilSealCompoundSystemDeflection]':
        '''List[OilSealCompoundSystemDeflection]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_2449.OilSealCompoundSystemDeflection))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_2451.PartToPartShearCouplingCompoundSystemDeflection]':
        '''List[PartToPartShearCouplingCompoundSystemDeflection]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_2451.PartToPartShearCouplingCompoundSystemDeflection))
        return value

    @property
    def planet_carriers(self) -> 'List[_2456.PlanetCarrierCompoundSystemDeflection]':
        '''List[PlanetCarrierCompoundSystemDeflection]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_2456.PlanetCarrierCompoundSystemDeflection))
        return value

    @property
    def point_loads(self) -> 'List[_2457.PointLoadCompoundSystemDeflection]':
        '''List[PointLoadCompoundSystemDeflection]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_2457.PointLoadCompoundSystemDeflection))
        return value

    @property
    def power_loads(self) -> 'List[_2458.PowerLoadCompoundSystemDeflection]':
        '''List[PowerLoadCompoundSystemDeflection]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_2458.PowerLoadCompoundSystemDeflection))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_2466.ShaftHubConnectionCompoundSystemDeflection]':
        '''List[ShaftHubConnectionCompoundSystemDeflection]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_2466.ShaftHubConnectionCompoundSystemDeflection))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_2460.RollingRingAssemblyCompoundSystemDeflection]':
        '''List[RollingRingAssemblyCompoundSystemDeflection]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_2460.RollingRingAssemblyCompoundSystemDeflection))
        return value

    @property
    def shafts(self) -> 'List[_2464.ShaftCompoundSystemDeflection]':
        '''List[ShaftCompoundSystemDeflection]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_2464.ShaftCompoundSystemDeflection))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_2471.SpiralBevelGearSetCompoundSystemDeflection]':
        '''List[SpiralBevelGearSetCompoundSystemDeflection]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_2471.SpiralBevelGearSetCompoundSystemDeflection))
        return value

    @property
    def spring_dampers(self) -> 'List[_2472.SpringDamperCompoundSystemDeflection]':
        '''List[SpringDamperCompoundSystemDeflection]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_2472.SpringDamperCompoundSystemDeflection))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_2477.StraightBevelDiffGearSetCompoundSystemDeflection]':
        '''List[StraightBevelDiffGearSetCompoundSystemDeflection]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_2477.StraightBevelDiffGearSetCompoundSystemDeflection))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_2480.StraightBevelGearSetCompoundSystemDeflection]':
        '''List[StraightBevelGearSetCompoundSystemDeflection]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_2480.StraightBevelGearSetCompoundSystemDeflection))
        return value

    @property
    def synchronisers(self) -> 'List[_2483.SynchroniserCompoundSystemDeflection]':
        '''List[SynchroniserCompoundSystemDeflection]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_2483.SynchroniserCompoundSystemDeflection))
        return value

    @property
    def torque_converters(self) -> 'List[_2487.TorqueConverterCompoundSystemDeflection]':
        '''List[TorqueConverterCompoundSystemDeflection]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_2487.TorqueConverterCompoundSystemDeflection))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_2491.UnbalancedMassCompoundSystemDeflection]':
        '''List[UnbalancedMassCompoundSystemDeflection]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_2491.UnbalancedMassCompoundSystemDeflection))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_2495.WormGearSetCompoundSystemDeflection]':
        '''List[WormGearSetCompoundSystemDeflection]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_2495.WormGearSetCompoundSystemDeflection))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_2498.ZerolBevelGearSetCompoundSystemDeflection]':
        '''List[ZerolBevelGearSetCompoundSystemDeflection]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_2498.ZerolBevelGearSetCompoundSystemDeflection))
        return value

    @property
    def rolling_bearings(self) -> 'List[_2383.BearingCompoundSystemDeflection]':
        '''List[BearingCompoundSystemDeflection]: 'RollingBearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingBearings, constructor.new(_2383.BearingCompoundSystemDeflection))
        return value
