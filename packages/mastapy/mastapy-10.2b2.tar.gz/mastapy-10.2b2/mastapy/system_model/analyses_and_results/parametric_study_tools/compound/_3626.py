'''_3626.py

AssemblyCompoundParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model import _1999
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.parametric_study_tools import _3489
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import (
    _3627, _3629, _3632, _3638,
    _3639, _3640, _3645, _3650,
    _3660, _3664, _3670, _3671,
    _3678, _3679, _3686, _3689,
    _3690, _3691, _3693, _3695,
    _3700, _3701, _3702, _3709,
    _3704, _3708, _3714, _3715,
    _3720, _3723, _3726, _3730,
    _3734, _3738, _3741, _3621
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'AssemblyCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyCompoundParametricStudyTool',)


class AssemblyCompoundParametricStudyTool(_3621.AbstractAssemblyCompoundParametricStudyTool):
    '''AssemblyCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyCompoundParametricStudyTool.TYPE'):
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
    def load_case_analyses_ready(self) -> 'List[_3489.AssemblyParametricStudyTool]':
        '''List[AssemblyParametricStudyTool]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3489.AssemblyParametricStudyTool))
        return value

    @property
    def assembly_parametric_study_tool_load_cases(self) -> 'List[_3489.AssemblyParametricStudyTool]':
        '''List[AssemblyParametricStudyTool]: 'AssemblyParametricStudyToolLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyParametricStudyToolLoadCases, constructor.new(_3489.AssemblyParametricStudyTool))
        return value

    @property
    def bearings(self) -> 'List[_3627.BearingCompoundParametricStudyTool]':
        '''List[BearingCompoundParametricStudyTool]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_3627.BearingCompoundParametricStudyTool))
        return value

    @property
    def belt_drives(self) -> 'List[_3629.BeltDriveCompoundParametricStudyTool]':
        '''List[BeltDriveCompoundParametricStudyTool]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_3629.BeltDriveCompoundParametricStudyTool))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_3632.BevelDifferentialGearSetCompoundParametricStudyTool]':
        '''List[BevelDifferentialGearSetCompoundParametricStudyTool]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_3632.BevelDifferentialGearSetCompoundParametricStudyTool))
        return value

    @property
    def bolts(self) -> 'List[_3638.BoltCompoundParametricStudyTool]':
        '''List[BoltCompoundParametricStudyTool]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_3638.BoltCompoundParametricStudyTool))
        return value

    @property
    def bolted_joints(self) -> 'List[_3639.BoltedJointCompoundParametricStudyTool]':
        '''List[BoltedJointCompoundParametricStudyTool]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_3639.BoltedJointCompoundParametricStudyTool))
        return value

    @property
    def clutches(self) -> 'List[_3640.ClutchCompoundParametricStudyTool]':
        '''List[ClutchCompoundParametricStudyTool]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_3640.ClutchCompoundParametricStudyTool))
        return value

    @property
    def concept_couplings(self) -> 'List[_3645.ConceptCouplingCompoundParametricStudyTool]':
        '''List[ConceptCouplingCompoundParametricStudyTool]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_3645.ConceptCouplingCompoundParametricStudyTool))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_3650.ConceptGearSetCompoundParametricStudyTool]':
        '''List[ConceptGearSetCompoundParametricStudyTool]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_3650.ConceptGearSetCompoundParametricStudyTool))
        return value

    @property
    def cv_ts(self) -> 'List[_3660.CVTCompoundParametricStudyTool]':
        '''List[CVTCompoundParametricStudyTool]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_3660.CVTCompoundParametricStudyTool))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_3664.CylindricalGearSetCompoundParametricStudyTool]':
        '''List[CylindricalGearSetCompoundParametricStudyTool]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_3664.CylindricalGearSetCompoundParametricStudyTool))
        return value

    @property
    def face_gear_sets(self) -> 'List[_3670.FaceGearSetCompoundParametricStudyTool]':
        '''List[FaceGearSetCompoundParametricStudyTool]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_3670.FaceGearSetCompoundParametricStudyTool))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_3671.FlexiblePinAssemblyCompoundParametricStudyTool]':
        '''List[FlexiblePinAssemblyCompoundParametricStudyTool]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_3671.FlexiblePinAssemblyCompoundParametricStudyTool))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_3678.HypoidGearSetCompoundParametricStudyTool]':
        '''List[HypoidGearSetCompoundParametricStudyTool]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_3678.HypoidGearSetCompoundParametricStudyTool))
        return value

    @property
    def imported_fe_components(self) -> 'List[_3679.ImportedFEComponentCompoundParametricStudyTool]':
        '''List[ImportedFEComponentCompoundParametricStudyTool]: 'ImportedFEComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ImportedFEComponents, constructor.new(_3679.ImportedFEComponentCompoundParametricStudyTool))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_3686.KlingelnbergCycloPalloidHypoidGearSetCompoundParametricStudyTool]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetCompoundParametricStudyTool]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_3686.KlingelnbergCycloPalloidHypoidGearSetCompoundParametricStudyTool))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_3689.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundParametricStudyTool]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetCompoundParametricStudyTool]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_3689.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundParametricStudyTool))
        return value

    @property
    def mass_discs(self) -> 'List[_3690.MassDiscCompoundParametricStudyTool]':
        '''List[MassDiscCompoundParametricStudyTool]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_3690.MassDiscCompoundParametricStudyTool))
        return value

    @property
    def measurement_components(self) -> 'List[_3691.MeasurementComponentCompoundParametricStudyTool]':
        '''List[MeasurementComponentCompoundParametricStudyTool]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_3691.MeasurementComponentCompoundParametricStudyTool))
        return value

    @property
    def oil_seals(self) -> 'List[_3693.OilSealCompoundParametricStudyTool]':
        '''List[OilSealCompoundParametricStudyTool]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_3693.OilSealCompoundParametricStudyTool))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_3695.PartToPartShearCouplingCompoundParametricStudyTool]':
        '''List[PartToPartShearCouplingCompoundParametricStudyTool]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_3695.PartToPartShearCouplingCompoundParametricStudyTool))
        return value

    @property
    def planet_carriers(self) -> 'List[_3700.PlanetCarrierCompoundParametricStudyTool]':
        '''List[PlanetCarrierCompoundParametricStudyTool]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_3700.PlanetCarrierCompoundParametricStudyTool))
        return value

    @property
    def point_loads(self) -> 'List[_3701.PointLoadCompoundParametricStudyTool]':
        '''List[PointLoadCompoundParametricStudyTool]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_3701.PointLoadCompoundParametricStudyTool))
        return value

    @property
    def power_loads(self) -> 'List[_3702.PowerLoadCompoundParametricStudyTool]':
        '''List[PowerLoadCompoundParametricStudyTool]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_3702.PowerLoadCompoundParametricStudyTool))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_3709.ShaftHubConnectionCompoundParametricStudyTool]':
        '''List[ShaftHubConnectionCompoundParametricStudyTool]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_3709.ShaftHubConnectionCompoundParametricStudyTool))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_3704.RollingRingAssemblyCompoundParametricStudyTool]':
        '''List[RollingRingAssemblyCompoundParametricStudyTool]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_3704.RollingRingAssemblyCompoundParametricStudyTool))
        return value

    @property
    def shafts(self) -> 'List[_3708.ShaftCompoundParametricStudyTool]':
        '''List[ShaftCompoundParametricStudyTool]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_3708.ShaftCompoundParametricStudyTool))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_3714.SpiralBevelGearSetCompoundParametricStudyTool]':
        '''List[SpiralBevelGearSetCompoundParametricStudyTool]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_3714.SpiralBevelGearSetCompoundParametricStudyTool))
        return value

    @property
    def spring_dampers(self) -> 'List[_3715.SpringDamperCompoundParametricStudyTool]':
        '''List[SpringDamperCompoundParametricStudyTool]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_3715.SpringDamperCompoundParametricStudyTool))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_3720.StraightBevelDiffGearSetCompoundParametricStudyTool]':
        '''List[StraightBevelDiffGearSetCompoundParametricStudyTool]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_3720.StraightBevelDiffGearSetCompoundParametricStudyTool))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_3723.StraightBevelGearSetCompoundParametricStudyTool]':
        '''List[StraightBevelGearSetCompoundParametricStudyTool]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_3723.StraightBevelGearSetCompoundParametricStudyTool))
        return value

    @property
    def synchronisers(self) -> 'List[_3726.SynchroniserCompoundParametricStudyTool]':
        '''List[SynchroniserCompoundParametricStudyTool]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_3726.SynchroniserCompoundParametricStudyTool))
        return value

    @property
    def torque_converters(self) -> 'List[_3730.TorqueConverterCompoundParametricStudyTool]':
        '''List[TorqueConverterCompoundParametricStudyTool]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_3730.TorqueConverterCompoundParametricStudyTool))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_3734.UnbalancedMassCompoundParametricStudyTool]':
        '''List[UnbalancedMassCompoundParametricStudyTool]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_3734.UnbalancedMassCompoundParametricStudyTool))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_3738.WormGearSetCompoundParametricStudyTool]':
        '''List[WormGearSetCompoundParametricStudyTool]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_3738.WormGearSetCompoundParametricStudyTool))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_3741.ZerolBevelGearSetCompoundParametricStudyTool]':
        '''List[ZerolBevelGearSetCompoundParametricStudyTool]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_3741.ZerolBevelGearSetCompoundParametricStudyTool))
        return value
