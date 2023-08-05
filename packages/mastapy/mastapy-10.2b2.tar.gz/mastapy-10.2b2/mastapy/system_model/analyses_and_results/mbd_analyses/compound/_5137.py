'''_5137.py

AssemblyCompoundMultiBodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _1999
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.mbd_analyses import _4993
from mastapy.system_model.analyses_and_results.mbd_analyses.compound import (
    _5138, _5140, _5143, _5149,
    _5150, _5151, _5156, _5161,
    _5171, _5175, _5181, _5182,
    _5189, _5190, _5197, _5200,
    _5201, _5202, _5204, _5206,
    _5211, _5212, _5213, _5220,
    _5215, _5219, _5225, _5226,
    _5231, _5234, _5237, _5241,
    _5245, _5249, _5252, _5132
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'AssemblyCompoundMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyCompoundMultiBodyDynamicsAnalysis',)


class AssemblyCompoundMultiBodyDynamicsAnalysis(_5132.AbstractAssemblyCompoundMultiBodyDynamicsAnalysis):
    '''AssemblyCompoundMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyCompoundMultiBodyDynamicsAnalysis.TYPE'):
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
    def load_case_analyses_ready(self) -> 'List[_4993.AssemblyMultiBodyDynamicsAnalysis]':
        '''List[AssemblyMultiBodyDynamicsAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4993.AssemblyMultiBodyDynamicsAnalysis))
        return value

    @property
    def assembly_multi_body_dynamics_analysis_load_cases(self) -> 'List[_4993.AssemblyMultiBodyDynamicsAnalysis]':
        '''List[AssemblyMultiBodyDynamicsAnalysis]: 'AssemblyMultiBodyDynamicsAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyMultiBodyDynamicsAnalysisLoadCases, constructor.new(_4993.AssemblyMultiBodyDynamicsAnalysis))
        return value

    @property
    def bearings(self) -> 'List[_5138.BearingCompoundMultiBodyDynamicsAnalysis]':
        '''List[BearingCompoundMultiBodyDynamicsAnalysis]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_5138.BearingCompoundMultiBodyDynamicsAnalysis))
        return value

    @property
    def belt_drives(self) -> 'List[_5140.BeltDriveCompoundMultiBodyDynamicsAnalysis]':
        '''List[BeltDriveCompoundMultiBodyDynamicsAnalysis]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_5140.BeltDriveCompoundMultiBodyDynamicsAnalysis))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_5143.BevelDifferentialGearSetCompoundMultiBodyDynamicsAnalysis]':
        '''List[BevelDifferentialGearSetCompoundMultiBodyDynamicsAnalysis]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_5143.BevelDifferentialGearSetCompoundMultiBodyDynamicsAnalysis))
        return value

    @property
    def bolts(self) -> 'List[_5149.BoltCompoundMultiBodyDynamicsAnalysis]':
        '''List[BoltCompoundMultiBodyDynamicsAnalysis]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_5149.BoltCompoundMultiBodyDynamicsAnalysis))
        return value

    @property
    def bolted_joints(self) -> 'List[_5150.BoltedJointCompoundMultiBodyDynamicsAnalysis]':
        '''List[BoltedJointCompoundMultiBodyDynamicsAnalysis]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_5150.BoltedJointCompoundMultiBodyDynamicsAnalysis))
        return value

    @property
    def clutches(self) -> 'List[_5151.ClutchCompoundMultiBodyDynamicsAnalysis]':
        '''List[ClutchCompoundMultiBodyDynamicsAnalysis]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_5151.ClutchCompoundMultiBodyDynamicsAnalysis))
        return value

    @property
    def concept_couplings(self) -> 'List[_5156.ConceptCouplingCompoundMultiBodyDynamicsAnalysis]':
        '''List[ConceptCouplingCompoundMultiBodyDynamicsAnalysis]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_5156.ConceptCouplingCompoundMultiBodyDynamicsAnalysis))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_5161.ConceptGearSetCompoundMultiBodyDynamicsAnalysis]':
        '''List[ConceptGearSetCompoundMultiBodyDynamicsAnalysis]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_5161.ConceptGearSetCompoundMultiBodyDynamicsAnalysis))
        return value

    @property
    def cv_ts(self) -> 'List[_5171.CVTCompoundMultiBodyDynamicsAnalysis]':
        '''List[CVTCompoundMultiBodyDynamicsAnalysis]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_5171.CVTCompoundMultiBodyDynamicsAnalysis))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_5175.CylindricalGearSetCompoundMultiBodyDynamicsAnalysis]':
        '''List[CylindricalGearSetCompoundMultiBodyDynamicsAnalysis]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_5175.CylindricalGearSetCompoundMultiBodyDynamicsAnalysis))
        return value

    @property
    def face_gear_sets(self) -> 'List[_5181.FaceGearSetCompoundMultiBodyDynamicsAnalysis]':
        '''List[FaceGearSetCompoundMultiBodyDynamicsAnalysis]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_5181.FaceGearSetCompoundMultiBodyDynamicsAnalysis))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_5182.FlexiblePinAssemblyCompoundMultiBodyDynamicsAnalysis]':
        '''List[FlexiblePinAssemblyCompoundMultiBodyDynamicsAnalysis]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_5182.FlexiblePinAssemblyCompoundMultiBodyDynamicsAnalysis))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_5189.HypoidGearSetCompoundMultiBodyDynamicsAnalysis]':
        '''List[HypoidGearSetCompoundMultiBodyDynamicsAnalysis]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_5189.HypoidGearSetCompoundMultiBodyDynamicsAnalysis))
        return value

    @property
    def imported_fe_components(self) -> 'List[_5190.ImportedFEComponentCompoundMultiBodyDynamicsAnalysis]':
        '''List[ImportedFEComponentCompoundMultiBodyDynamicsAnalysis]: 'ImportedFEComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ImportedFEComponents, constructor.new(_5190.ImportedFEComponentCompoundMultiBodyDynamicsAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_5197.KlingelnbergCycloPalloidHypoidGearSetCompoundMultiBodyDynamicsAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetCompoundMultiBodyDynamicsAnalysis]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_5197.KlingelnbergCycloPalloidHypoidGearSetCompoundMultiBodyDynamicsAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_5200.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundMultiBodyDynamicsAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetCompoundMultiBodyDynamicsAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_5200.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundMultiBodyDynamicsAnalysis))
        return value

    @property
    def mass_discs(self) -> 'List[_5201.MassDiscCompoundMultiBodyDynamicsAnalysis]':
        '''List[MassDiscCompoundMultiBodyDynamicsAnalysis]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_5201.MassDiscCompoundMultiBodyDynamicsAnalysis))
        return value

    @property
    def measurement_components(self) -> 'List[_5202.MeasurementComponentCompoundMultiBodyDynamicsAnalysis]':
        '''List[MeasurementComponentCompoundMultiBodyDynamicsAnalysis]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_5202.MeasurementComponentCompoundMultiBodyDynamicsAnalysis))
        return value

    @property
    def oil_seals(self) -> 'List[_5204.OilSealCompoundMultiBodyDynamicsAnalysis]':
        '''List[OilSealCompoundMultiBodyDynamicsAnalysis]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_5204.OilSealCompoundMultiBodyDynamicsAnalysis))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_5206.PartToPartShearCouplingCompoundMultiBodyDynamicsAnalysis]':
        '''List[PartToPartShearCouplingCompoundMultiBodyDynamicsAnalysis]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_5206.PartToPartShearCouplingCompoundMultiBodyDynamicsAnalysis))
        return value

    @property
    def planet_carriers(self) -> 'List[_5211.PlanetCarrierCompoundMultiBodyDynamicsAnalysis]':
        '''List[PlanetCarrierCompoundMultiBodyDynamicsAnalysis]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_5211.PlanetCarrierCompoundMultiBodyDynamicsAnalysis))
        return value

    @property
    def point_loads(self) -> 'List[_5212.PointLoadCompoundMultiBodyDynamicsAnalysis]':
        '''List[PointLoadCompoundMultiBodyDynamicsAnalysis]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_5212.PointLoadCompoundMultiBodyDynamicsAnalysis))
        return value

    @property
    def power_loads(self) -> 'List[_5213.PowerLoadCompoundMultiBodyDynamicsAnalysis]':
        '''List[PowerLoadCompoundMultiBodyDynamicsAnalysis]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_5213.PowerLoadCompoundMultiBodyDynamicsAnalysis))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_5220.ShaftHubConnectionCompoundMultiBodyDynamicsAnalysis]':
        '''List[ShaftHubConnectionCompoundMultiBodyDynamicsAnalysis]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_5220.ShaftHubConnectionCompoundMultiBodyDynamicsAnalysis))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_5215.RollingRingAssemblyCompoundMultiBodyDynamicsAnalysis]':
        '''List[RollingRingAssemblyCompoundMultiBodyDynamicsAnalysis]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_5215.RollingRingAssemblyCompoundMultiBodyDynamicsAnalysis))
        return value

    @property
    def shafts(self) -> 'List[_5219.ShaftCompoundMultiBodyDynamicsAnalysis]':
        '''List[ShaftCompoundMultiBodyDynamicsAnalysis]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_5219.ShaftCompoundMultiBodyDynamicsAnalysis))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_5225.SpiralBevelGearSetCompoundMultiBodyDynamicsAnalysis]':
        '''List[SpiralBevelGearSetCompoundMultiBodyDynamicsAnalysis]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_5225.SpiralBevelGearSetCompoundMultiBodyDynamicsAnalysis))
        return value

    @property
    def spring_dampers(self) -> 'List[_5226.SpringDamperCompoundMultiBodyDynamicsAnalysis]':
        '''List[SpringDamperCompoundMultiBodyDynamicsAnalysis]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_5226.SpringDamperCompoundMultiBodyDynamicsAnalysis))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_5231.StraightBevelDiffGearSetCompoundMultiBodyDynamicsAnalysis]':
        '''List[StraightBevelDiffGearSetCompoundMultiBodyDynamicsAnalysis]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_5231.StraightBevelDiffGearSetCompoundMultiBodyDynamicsAnalysis))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_5234.StraightBevelGearSetCompoundMultiBodyDynamicsAnalysis]':
        '''List[StraightBevelGearSetCompoundMultiBodyDynamicsAnalysis]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_5234.StraightBevelGearSetCompoundMultiBodyDynamicsAnalysis))
        return value

    @property
    def synchronisers(self) -> 'List[_5237.SynchroniserCompoundMultiBodyDynamicsAnalysis]':
        '''List[SynchroniserCompoundMultiBodyDynamicsAnalysis]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_5237.SynchroniserCompoundMultiBodyDynamicsAnalysis))
        return value

    @property
    def torque_converters(self) -> 'List[_5241.TorqueConverterCompoundMultiBodyDynamicsAnalysis]':
        '''List[TorqueConverterCompoundMultiBodyDynamicsAnalysis]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_5241.TorqueConverterCompoundMultiBodyDynamicsAnalysis))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_5245.UnbalancedMassCompoundMultiBodyDynamicsAnalysis]':
        '''List[UnbalancedMassCompoundMultiBodyDynamicsAnalysis]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_5245.UnbalancedMassCompoundMultiBodyDynamicsAnalysis))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_5249.WormGearSetCompoundMultiBodyDynamicsAnalysis]':
        '''List[WormGearSetCompoundMultiBodyDynamicsAnalysis]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_5249.WormGearSetCompoundMultiBodyDynamicsAnalysis))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_5252.ZerolBevelGearSetCompoundMultiBodyDynamicsAnalysis]':
        '''List[ZerolBevelGearSetCompoundMultiBodyDynamicsAnalysis]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_5252.ZerolBevelGearSetCompoundMultiBodyDynamicsAnalysis))
        return value
