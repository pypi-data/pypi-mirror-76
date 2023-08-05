'''_2218.py

CompoundModalAnalysisAnalysis
'''


from typing import Iterable

from mastapy.system_model.part_model import (
    _2000, _2001, _2004, _2006,
    _2007, _2008, _2011, _2012,
    _2015, _2016, _1999, _2017,
    _2020, _2024, _2025, _2026,
    _2028, _2030, _2031, _2033,
    _2034, _2036, _2038, _2039,
    _2040
)
from mastapy.system_model.analyses_and_results.modal_analyses.compound import (
    _4866, _4867, _4872, _4883,
    _4884, _4889, _4900, _4911,
    _4912, _4916, _4871, _4920,
    _4924, _4935, _4936, _4937,
    _4938, _4939, _4945, _4946,
    _4947, _4952, _4956, _4979,
    _4980, _4953, _4893, _4895,
    _4913, _4915, _4868, _4870,
    _4875, _4877, _4878, _4879,
    _4880, _4882, _4896, _4898,
    _4907, _4909, _4910, _4917,
    _4919, _4921, _4923, _4926,
    _4928, _4929, _4931, _4932,
    _4934, _4944, _4957, _4959,
    _4963, _4965, _4966, _4968,
    _4969, _4970, _4981, _4983,
    _4984, _4986, _4940, _4942,
    _4874, _4885, _4887, _4890,
    _4892, _4901, _4903, _4905,
    _4906, _4948, _4954, _4950,
    _4949, _4960, _4962, _4971,
    _4972, _4973, _4974, _4975,
    _4977, _4978, _4904, _4873,
    _4888, _4899, _4925, _4943,
    _4951, _4955, _4876, _4894,
    _4914, _4964, _4881, _4897,
    _4869, _4908, _4922, _4927,
    _4930, _4933, _4958, _4967,
    _4982, _4985, _4918, _4941,
    _4886, _4891, _4902, _4961,
    _4976
)
from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model.shaft_model import _2043
from mastapy.system_model.part_model.gears import (
    _2081, _2082, _2088, _2089,
    _2073, _2074, _2075, _2076,
    _2077, _2078, _2079, _2080,
    _2083, _2084, _2085, _2086,
    _2087, _2090, _2092, _2094,
    _2095, _2096, _2097, _2098,
    _2099, _2100, _2101, _2102,
    _2103, _2104, _2105, _2106,
    _2107, _2108, _2109, _2110,
    _2111, _2112, _2113, _2114
)
from mastapy.system_model.part_model.couplings import (
    _2143, _2144, _2132, _2134,
    _2135, _2137, _2138, _2139,
    _2140, _2141, _2142, _2145,
    _2153, _2151, _2152, _2154,
    _2155, _2156, _2158, _2159,
    _2160, _2161, _2162, _2164
)
from mastapy.system_model.connections_and_sockets import (
    _1856, _1851, _1852, _1855,
    _1864, _1867, _1871, _1875
)
from mastapy.system_model.connections_and_sockets.gears import (
    _1881, _1885, _1891, _1905,
    _1883, _1887, _1879, _1889,
    _1895, _1898, _1899, _1900,
    _1903, _1907, _1909, _1911,
    _1893
)
from mastapy.system_model.connections_and_sockets.couplings import (
    _1919, _1913, _1915, _1917,
    _1921, _1923
)
from mastapy.system_model.analyses_and_results import _2173
from mastapy._internal.python_net import python_net_import

_COMPOUND_MODAL_ANALYSIS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults', 'CompoundModalAnalysisAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CompoundModalAnalysisAnalysis',)


class CompoundModalAnalysisAnalysis(_2173.CompoundAnalysis):
    '''CompoundModalAnalysisAnalysis

    This is a mastapy class.
    '''

    TYPE = _COMPOUND_MODAL_ANALYSIS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CompoundModalAnalysisAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    def results_for_abstract_assembly(self, design_entity: '_2000.AbstractAssembly') -> 'Iterable[_4866.AbstractAssemblyCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.AbstractAssemblyCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4866.AbstractAssemblyCompoundModalAnalysis))

    def results_for_abstract_shaft_or_housing(self, design_entity: '_2001.AbstractShaftOrHousing') -> 'Iterable[_4867.AbstractShaftOrHousingCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractShaftOrHousing)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.AbstractShaftOrHousingCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4867.AbstractShaftOrHousingCompoundModalAnalysis))

    def results_for_bearing(self, design_entity: '_2004.Bearing') -> 'Iterable[_4872.BearingCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bearing)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.BearingCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4872.BearingCompoundModalAnalysis))

    def results_for_bolt(self, design_entity: '_2006.Bolt') -> 'Iterable[_4883.BoltCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bolt)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.BoltCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4883.BoltCompoundModalAnalysis))

    def results_for_bolted_joint(self, design_entity: '_2007.BoltedJoint') -> 'Iterable[_4884.BoltedJointCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.BoltedJoint)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.BoltedJointCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4884.BoltedJointCompoundModalAnalysis))

    def results_for_component(self, design_entity: '_2008.Component') -> 'Iterable[_4889.ComponentCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Component)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.ComponentCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4889.ComponentCompoundModalAnalysis))

    def results_for_connector(self, design_entity: '_2011.Connector') -> 'Iterable[_4900.ConnectorCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Connector)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.ConnectorCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4900.ConnectorCompoundModalAnalysis))

    def results_for_datum(self, design_entity: '_2012.Datum') -> 'Iterable[_4911.DatumCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Datum)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.DatumCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4911.DatumCompoundModalAnalysis))

    def results_for_external_cad_model(self, design_entity: '_2015.ExternalCADModel') -> 'Iterable[_4912.ExternalCADModelCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ExternalCADModel)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.ExternalCADModelCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4912.ExternalCADModelCompoundModalAnalysis))

    def results_for_flexible_pin_assembly(self, design_entity: '_2016.FlexiblePinAssembly') -> 'Iterable[_4916.FlexiblePinAssemblyCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.FlexiblePinAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.FlexiblePinAssemblyCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4916.FlexiblePinAssemblyCompoundModalAnalysis))

    def results_for_assembly(self, design_entity: '_1999.Assembly') -> 'Iterable[_4871.AssemblyCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Assembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.AssemblyCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4871.AssemblyCompoundModalAnalysis))

    def results_for_guide_dxf_model(self, design_entity: '_2017.GuideDxfModel') -> 'Iterable[_4920.GuideDxfModelCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.GuideDxfModel)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.GuideDxfModelCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4920.GuideDxfModelCompoundModalAnalysis))

    def results_for_imported_fe_component(self, design_entity: '_2020.ImportedFEComponent') -> 'Iterable[_4924.ImportedFEComponentCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ImportedFEComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.ImportedFEComponentCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4924.ImportedFEComponentCompoundModalAnalysis))

    def results_for_mass_disc(self, design_entity: '_2024.MassDisc') -> 'Iterable[_4935.MassDiscCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MassDisc)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.MassDiscCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4935.MassDiscCompoundModalAnalysis))

    def results_for_measurement_component(self, design_entity: '_2025.MeasurementComponent') -> 'Iterable[_4936.MeasurementComponentCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MeasurementComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.MeasurementComponentCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4936.MeasurementComponentCompoundModalAnalysis))

    def results_for_mountable_component(self, design_entity: '_2026.MountableComponent') -> 'Iterable[_4937.MountableComponentCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MountableComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.MountableComponentCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4937.MountableComponentCompoundModalAnalysis))

    def results_for_oil_seal(self, design_entity: '_2028.OilSeal') -> 'Iterable[_4938.OilSealCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.OilSeal)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.OilSealCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4938.OilSealCompoundModalAnalysis))

    def results_for_part(self, design_entity: '_2030.Part') -> 'Iterable[_4939.PartCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Part)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.PartCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4939.PartCompoundModalAnalysis))

    def results_for_planet_carrier(self, design_entity: '_2031.PlanetCarrier') -> 'Iterable[_4945.PlanetCarrierCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PlanetCarrier)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.PlanetCarrierCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4945.PlanetCarrierCompoundModalAnalysis))

    def results_for_point_load(self, design_entity: '_2033.PointLoad') -> 'Iterable[_4946.PointLoadCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PointLoad)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.PointLoadCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4946.PointLoadCompoundModalAnalysis))

    def results_for_power_load(self, design_entity: '_2034.PowerLoad') -> 'Iterable[_4947.PowerLoadCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PowerLoad)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.PowerLoadCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4947.PowerLoadCompoundModalAnalysis))

    def results_for_root_assembly(self, design_entity: '_2036.RootAssembly') -> 'Iterable[_4952.RootAssemblyCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.RootAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.RootAssemblyCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4952.RootAssemblyCompoundModalAnalysis))

    def results_for_specialised_assembly(self, design_entity: '_2038.SpecialisedAssembly') -> 'Iterable[_4956.SpecialisedAssemblyCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.SpecialisedAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.SpecialisedAssemblyCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4956.SpecialisedAssemblyCompoundModalAnalysis))

    def results_for_unbalanced_mass(self, design_entity: '_2039.UnbalancedMass') -> 'Iterable[_4979.UnbalancedMassCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.UnbalancedMass)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.UnbalancedMassCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4979.UnbalancedMassCompoundModalAnalysis))

    def results_for_virtual_component(self, design_entity: '_2040.VirtualComponent') -> 'Iterable[_4980.VirtualComponentCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.VirtualComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.VirtualComponentCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4980.VirtualComponentCompoundModalAnalysis))

    def results_for_shaft(self, design_entity: '_2043.Shaft') -> 'Iterable[_4953.ShaftCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.shaft_model.Shaft)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.ShaftCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4953.ShaftCompoundModalAnalysis))

    def results_for_concept_gear(self, design_entity: '_2081.ConceptGear') -> 'Iterable[_4893.ConceptGearCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.ConceptGearCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4893.ConceptGearCompoundModalAnalysis))

    def results_for_concept_gear_set(self, design_entity: '_2082.ConceptGearSet') -> 'Iterable[_4895.ConceptGearSetCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.ConceptGearSetCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4895.ConceptGearSetCompoundModalAnalysis))

    def results_for_face_gear(self, design_entity: '_2088.FaceGear') -> 'Iterable[_4913.FaceGearCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.FaceGearCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4913.FaceGearCompoundModalAnalysis))

    def results_for_face_gear_set(self, design_entity: '_2089.FaceGearSet') -> 'Iterable[_4915.FaceGearSetCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.FaceGearSetCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4915.FaceGearSetCompoundModalAnalysis))

    def results_for_agma_gleason_conical_gear(self, design_entity: '_2073.AGMAGleasonConicalGear') -> 'Iterable[_4868.AGMAGleasonConicalGearCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.AGMAGleasonConicalGearCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4868.AGMAGleasonConicalGearCompoundModalAnalysis))

    def results_for_agma_gleason_conical_gear_set(self, design_entity: '_2074.AGMAGleasonConicalGearSet') -> 'Iterable[_4870.AGMAGleasonConicalGearSetCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.AGMAGleasonConicalGearSetCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4870.AGMAGleasonConicalGearSetCompoundModalAnalysis))

    def results_for_bevel_differential_gear(self, design_entity: '_2075.BevelDifferentialGear') -> 'Iterable[_4875.BevelDifferentialGearCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.BevelDifferentialGearCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4875.BevelDifferentialGearCompoundModalAnalysis))

    def results_for_bevel_differential_gear_set(self, design_entity: '_2076.BevelDifferentialGearSet') -> 'Iterable[_4877.BevelDifferentialGearSetCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.BevelDifferentialGearSetCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4877.BevelDifferentialGearSetCompoundModalAnalysis))

    def results_for_bevel_differential_planet_gear(self, design_entity: '_2077.BevelDifferentialPlanetGear') -> 'Iterable[_4878.BevelDifferentialPlanetGearCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialPlanetGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.BevelDifferentialPlanetGearCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4878.BevelDifferentialPlanetGearCompoundModalAnalysis))

    def results_for_bevel_differential_sun_gear(self, design_entity: '_2078.BevelDifferentialSunGear') -> 'Iterable[_4879.BevelDifferentialSunGearCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialSunGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.BevelDifferentialSunGearCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4879.BevelDifferentialSunGearCompoundModalAnalysis))

    def results_for_bevel_gear(self, design_entity: '_2079.BevelGear') -> 'Iterable[_4880.BevelGearCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.BevelGearCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4880.BevelGearCompoundModalAnalysis))

    def results_for_bevel_gear_set(self, design_entity: '_2080.BevelGearSet') -> 'Iterable[_4882.BevelGearSetCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.BevelGearSetCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4882.BevelGearSetCompoundModalAnalysis))

    def results_for_conical_gear(self, design_entity: '_2083.ConicalGear') -> 'Iterable[_4896.ConicalGearCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.ConicalGearCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4896.ConicalGearCompoundModalAnalysis))

    def results_for_conical_gear_set(self, design_entity: '_2084.ConicalGearSet') -> 'Iterable[_4898.ConicalGearSetCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.ConicalGearSetCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4898.ConicalGearSetCompoundModalAnalysis))

    def results_for_cylindrical_gear(self, design_entity: '_2085.CylindricalGear') -> 'Iterable[_4907.CylindricalGearCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.CylindricalGearCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4907.CylindricalGearCompoundModalAnalysis))

    def results_for_cylindrical_gear_set(self, design_entity: '_2086.CylindricalGearSet') -> 'Iterable[_4909.CylindricalGearSetCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.CylindricalGearSetCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4909.CylindricalGearSetCompoundModalAnalysis))

    def results_for_cylindrical_planet_gear(self, design_entity: '_2087.CylindricalPlanetGear') -> 'Iterable[_4910.CylindricalPlanetGearCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalPlanetGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.CylindricalPlanetGearCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4910.CylindricalPlanetGearCompoundModalAnalysis))

    def results_for_gear(self, design_entity: '_2090.Gear') -> 'Iterable[_4917.GearCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.Gear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.GearCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4917.GearCompoundModalAnalysis))

    def results_for_gear_set(self, design_entity: '_2092.GearSet') -> 'Iterable[_4919.GearSetCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.GearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.GearSetCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4919.GearSetCompoundModalAnalysis))

    def results_for_hypoid_gear(self, design_entity: '_2094.HypoidGear') -> 'Iterable[_4921.HypoidGearCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.HypoidGearCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4921.HypoidGearCompoundModalAnalysis))

    def results_for_hypoid_gear_set(self, design_entity: '_2095.HypoidGearSet') -> 'Iterable[_4923.HypoidGearSetCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.HypoidGearSetCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4923.HypoidGearSetCompoundModalAnalysis))

    def results_for_klingelnberg_cyclo_palloid_conical_gear(self, design_entity: '_2096.KlingelnbergCycloPalloidConicalGear') -> 'Iterable[_4926.KlingelnbergCycloPalloidConicalGearCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.KlingelnbergCycloPalloidConicalGearCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4926.KlingelnbergCycloPalloidConicalGearCompoundModalAnalysis))

    def results_for_klingelnberg_cyclo_palloid_conical_gear_set(self, design_entity: '_2097.KlingelnbergCycloPalloidConicalGearSet') -> 'Iterable[_4928.KlingelnbergCycloPalloidConicalGearSetCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.KlingelnbergCycloPalloidConicalGearSetCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4928.KlingelnbergCycloPalloidConicalGearSetCompoundModalAnalysis))

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear(self, design_entity: '_2098.KlingelnbergCycloPalloidHypoidGear') -> 'Iterable[_4929.KlingelnbergCycloPalloidHypoidGearCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.KlingelnbergCycloPalloidHypoidGearCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4929.KlingelnbergCycloPalloidHypoidGearCompoundModalAnalysis))

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_set(self, design_entity: '_2099.KlingelnbergCycloPalloidHypoidGearSet') -> 'Iterable[_4931.KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4931.KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysis))

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear(self, design_entity: '_2100.KlingelnbergCycloPalloidSpiralBevelGear') -> 'Iterable[_4932.KlingelnbergCycloPalloidSpiralBevelGearCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.KlingelnbergCycloPalloidSpiralBevelGearCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4932.KlingelnbergCycloPalloidSpiralBevelGearCompoundModalAnalysis))

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self, design_entity: '_2101.KlingelnbergCycloPalloidSpiralBevelGearSet') -> 'Iterable[_4934.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4934.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysis))

    def results_for_planetary_gear_set(self, design_entity: '_2102.PlanetaryGearSet') -> 'Iterable[_4944.PlanetaryGearSetCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.PlanetaryGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.PlanetaryGearSetCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4944.PlanetaryGearSetCompoundModalAnalysis))

    def results_for_spiral_bevel_gear(self, design_entity: '_2103.SpiralBevelGear') -> 'Iterable[_4957.SpiralBevelGearCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.SpiralBevelGearCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4957.SpiralBevelGearCompoundModalAnalysis))

    def results_for_spiral_bevel_gear_set(self, design_entity: '_2104.SpiralBevelGearSet') -> 'Iterable[_4959.SpiralBevelGearSetCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.SpiralBevelGearSetCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4959.SpiralBevelGearSetCompoundModalAnalysis))

    def results_for_straight_bevel_diff_gear(self, design_entity: '_2105.StraightBevelDiffGear') -> 'Iterable[_4963.StraightBevelDiffGearCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.StraightBevelDiffGearCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4963.StraightBevelDiffGearCompoundModalAnalysis))

    def results_for_straight_bevel_diff_gear_set(self, design_entity: '_2106.StraightBevelDiffGearSet') -> 'Iterable[_4965.StraightBevelDiffGearSetCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.StraightBevelDiffGearSetCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4965.StraightBevelDiffGearSetCompoundModalAnalysis))

    def results_for_straight_bevel_gear(self, design_entity: '_2107.StraightBevelGear') -> 'Iterable[_4966.StraightBevelGearCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.StraightBevelGearCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4966.StraightBevelGearCompoundModalAnalysis))

    def results_for_straight_bevel_gear_set(self, design_entity: '_2108.StraightBevelGearSet') -> 'Iterable[_4968.StraightBevelGearSetCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.StraightBevelGearSetCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4968.StraightBevelGearSetCompoundModalAnalysis))

    def results_for_straight_bevel_planet_gear(self, design_entity: '_2109.StraightBevelPlanetGear') -> 'Iterable[_4969.StraightBevelPlanetGearCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelPlanetGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.StraightBevelPlanetGearCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4969.StraightBevelPlanetGearCompoundModalAnalysis))

    def results_for_straight_bevel_sun_gear(self, design_entity: '_2110.StraightBevelSunGear') -> 'Iterable[_4970.StraightBevelSunGearCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelSunGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.StraightBevelSunGearCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4970.StraightBevelSunGearCompoundModalAnalysis))

    def results_for_worm_gear(self, design_entity: '_2111.WormGear') -> 'Iterable[_4981.WormGearCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.WormGearCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4981.WormGearCompoundModalAnalysis))

    def results_for_worm_gear_set(self, design_entity: '_2112.WormGearSet') -> 'Iterable[_4983.WormGearSetCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.WormGearSetCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4983.WormGearSetCompoundModalAnalysis))

    def results_for_zerol_bevel_gear(self, design_entity: '_2113.ZerolBevelGear') -> 'Iterable[_4984.ZerolBevelGearCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.ZerolBevelGearCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4984.ZerolBevelGearCompoundModalAnalysis))

    def results_for_zerol_bevel_gear_set(self, design_entity: '_2114.ZerolBevelGearSet') -> 'Iterable[_4986.ZerolBevelGearSetCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.ZerolBevelGearSetCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4986.ZerolBevelGearSetCompoundModalAnalysis))

    def results_for_part_to_part_shear_coupling(self, design_entity: '_2143.PartToPartShearCoupling') -> 'Iterable[_4940.PartToPartShearCouplingCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCoupling)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.PartToPartShearCouplingCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4940.PartToPartShearCouplingCompoundModalAnalysis))

    def results_for_part_to_part_shear_coupling_half(self, design_entity: '_2144.PartToPartShearCouplingHalf') -> 'Iterable[_4942.PartToPartShearCouplingHalfCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCouplingHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.PartToPartShearCouplingHalfCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4942.PartToPartShearCouplingHalfCompoundModalAnalysis))

    def results_for_belt_drive(self, design_entity: '_2132.BeltDrive') -> 'Iterable[_4874.BeltDriveCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.BeltDrive)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.BeltDriveCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4874.BeltDriveCompoundModalAnalysis))

    def results_for_clutch(self, design_entity: '_2134.Clutch') -> 'Iterable[_4885.ClutchCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Clutch)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.ClutchCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4885.ClutchCompoundModalAnalysis))

    def results_for_clutch_half(self, design_entity: '_2135.ClutchHalf') -> 'Iterable[_4887.ClutchHalfCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ClutchHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.ClutchHalfCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4887.ClutchHalfCompoundModalAnalysis))

    def results_for_concept_coupling(self, design_entity: '_2137.ConceptCoupling') -> 'Iterable[_4890.ConceptCouplingCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCoupling)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.ConceptCouplingCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4890.ConceptCouplingCompoundModalAnalysis))

    def results_for_concept_coupling_half(self, design_entity: '_2138.ConceptCouplingHalf') -> 'Iterable[_4892.ConceptCouplingHalfCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCouplingHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.ConceptCouplingHalfCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4892.ConceptCouplingHalfCompoundModalAnalysis))

    def results_for_coupling(self, design_entity: '_2139.Coupling') -> 'Iterable[_4901.CouplingCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Coupling)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.CouplingCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4901.CouplingCompoundModalAnalysis))

    def results_for_coupling_half(self, design_entity: '_2140.CouplingHalf') -> 'Iterable[_4903.CouplingHalfCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CouplingHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.CouplingHalfCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4903.CouplingHalfCompoundModalAnalysis))

    def results_for_cvt(self, design_entity: '_2141.CVT') -> 'Iterable[_4905.CVTCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVT)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.CVTCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4905.CVTCompoundModalAnalysis))

    def results_for_cvt_pulley(self, design_entity: '_2142.CVTPulley') -> 'Iterable[_4906.CVTPulleyCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVTPulley)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.CVTPulleyCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4906.CVTPulleyCompoundModalAnalysis))

    def results_for_pulley(self, design_entity: '_2145.Pulley') -> 'Iterable[_4948.PulleyCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Pulley)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.PulleyCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4948.PulleyCompoundModalAnalysis))

    def results_for_shaft_hub_connection(self, design_entity: '_2153.ShaftHubConnection') -> 'Iterable[_4954.ShaftHubConnectionCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ShaftHubConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.ShaftHubConnectionCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4954.ShaftHubConnectionCompoundModalAnalysis))

    def results_for_rolling_ring(self, design_entity: '_2151.RollingRing') -> 'Iterable[_4950.RollingRingCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRing)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.RollingRingCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4950.RollingRingCompoundModalAnalysis))

    def results_for_rolling_ring_assembly(self, design_entity: '_2152.RollingRingAssembly') -> 'Iterable[_4949.RollingRingAssemblyCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRingAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.RollingRingAssemblyCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4949.RollingRingAssemblyCompoundModalAnalysis))

    def results_for_spring_damper(self, design_entity: '_2154.SpringDamper') -> 'Iterable[_4960.SpringDamperCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamper)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.SpringDamperCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4960.SpringDamperCompoundModalAnalysis))

    def results_for_spring_damper_half(self, design_entity: '_2155.SpringDamperHalf') -> 'Iterable[_4962.SpringDamperHalfCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamperHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.SpringDamperHalfCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4962.SpringDamperHalfCompoundModalAnalysis))

    def results_for_synchroniser(self, design_entity: '_2156.Synchroniser') -> 'Iterable[_4971.SynchroniserCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Synchroniser)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.SynchroniserCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4971.SynchroniserCompoundModalAnalysis))

    def results_for_synchroniser_half(self, design_entity: '_2158.SynchroniserHalf') -> 'Iterable[_4972.SynchroniserHalfCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.SynchroniserHalfCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4972.SynchroniserHalfCompoundModalAnalysis))

    def results_for_synchroniser_part(self, design_entity: '_2159.SynchroniserPart') -> 'Iterable[_4973.SynchroniserPartCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserPart)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.SynchroniserPartCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4973.SynchroniserPartCompoundModalAnalysis))

    def results_for_synchroniser_sleeve(self, design_entity: '_2160.SynchroniserSleeve') -> 'Iterable[_4974.SynchroniserSleeveCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserSleeve)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.SynchroniserSleeveCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4974.SynchroniserSleeveCompoundModalAnalysis))

    def results_for_torque_converter(self, design_entity: '_2161.TorqueConverter') -> 'Iterable[_4975.TorqueConverterCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverter)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.TorqueConverterCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4975.TorqueConverterCompoundModalAnalysis))

    def results_for_torque_converter_pump(self, design_entity: '_2162.TorqueConverterPump') -> 'Iterable[_4977.TorqueConverterPumpCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterPump)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.TorqueConverterPumpCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4977.TorqueConverterPumpCompoundModalAnalysis))

    def results_for_torque_converter_turbine(self, design_entity: '_2164.TorqueConverterTurbine') -> 'Iterable[_4978.TorqueConverterTurbineCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterTurbine)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.TorqueConverterTurbineCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4978.TorqueConverterTurbineCompoundModalAnalysis))

    def results_for_cvt_belt_connection(self, design_entity: '_1856.CVTBeltConnection') -> 'Iterable[_4904.CVTBeltConnectionCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CVTBeltConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.CVTBeltConnectionCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4904.CVTBeltConnectionCompoundModalAnalysis))

    def results_for_belt_connection(self, design_entity: '_1851.BeltConnection') -> 'Iterable[_4873.BeltConnectionCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.BeltConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.BeltConnectionCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4873.BeltConnectionCompoundModalAnalysis))

    def results_for_coaxial_connection(self, design_entity: '_1852.CoaxialConnection') -> 'Iterable[_4888.CoaxialConnectionCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CoaxialConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.CoaxialConnectionCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4888.CoaxialConnectionCompoundModalAnalysis))

    def results_for_connection(self, design_entity: '_1855.Connection') -> 'Iterable[_4899.ConnectionCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.Connection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.ConnectionCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4899.ConnectionCompoundModalAnalysis))

    def results_for_inter_mountable_component_connection(self, design_entity: '_1864.InterMountableComponentConnection') -> 'Iterable[_4925.InterMountableComponentConnectionCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.InterMountableComponentConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.InterMountableComponentConnectionCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4925.InterMountableComponentConnectionCompoundModalAnalysis))

    def results_for_planetary_connection(self, design_entity: '_1867.PlanetaryConnection') -> 'Iterable[_4943.PlanetaryConnectionCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.PlanetaryConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.PlanetaryConnectionCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4943.PlanetaryConnectionCompoundModalAnalysis))

    def results_for_rolling_ring_connection(self, design_entity: '_1871.RollingRingConnection') -> 'Iterable[_4951.RollingRingConnectionCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.RollingRingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.RollingRingConnectionCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4951.RollingRingConnectionCompoundModalAnalysis))

    def results_for_shaft_to_mountable_component_connection(self, design_entity: '_1875.ShaftToMountableComponentConnection') -> 'Iterable[_4955.ShaftToMountableComponentConnectionCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.ShaftToMountableComponentConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.ShaftToMountableComponentConnectionCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4955.ShaftToMountableComponentConnectionCompoundModalAnalysis))

    def results_for_bevel_differential_gear_mesh(self, design_entity: '_1881.BevelDifferentialGearMesh') -> 'Iterable[_4876.BevelDifferentialGearMeshCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelDifferentialGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.BevelDifferentialGearMeshCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4876.BevelDifferentialGearMeshCompoundModalAnalysis))

    def results_for_concept_gear_mesh(self, design_entity: '_1885.ConceptGearMesh') -> 'Iterable[_4894.ConceptGearMeshCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConceptGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.ConceptGearMeshCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4894.ConceptGearMeshCompoundModalAnalysis))

    def results_for_face_gear_mesh(self, design_entity: '_1891.FaceGearMesh') -> 'Iterable[_4914.FaceGearMeshCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.FaceGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.FaceGearMeshCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4914.FaceGearMeshCompoundModalAnalysis))

    def results_for_straight_bevel_diff_gear_mesh(self, design_entity: '_1905.StraightBevelDiffGearMesh') -> 'Iterable[_4964.StraightBevelDiffGearMeshCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelDiffGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.StraightBevelDiffGearMeshCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4964.StraightBevelDiffGearMeshCompoundModalAnalysis))

    def results_for_bevel_gear_mesh(self, design_entity: '_1883.BevelGearMesh') -> 'Iterable[_4881.BevelGearMeshCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.BevelGearMeshCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4881.BevelGearMeshCompoundModalAnalysis))

    def results_for_conical_gear_mesh(self, design_entity: '_1887.ConicalGearMesh') -> 'Iterable[_4897.ConicalGearMeshCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConicalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.ConicalGearMeshCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4897.ConicalGearMeshCompoundModalAnalysis))

    def results_for_agma_gleason_conical_gear_mesh(self, design_entity: '_1879.AGMAGleasonConicalGearMesh') -> 'Iterable[_4869.AGMAGleasonConicalGearMeshCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.AGMAGleasonConicalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.AGMAGleasonConicalGearMeshCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4869.AGMAGleasonConicalGearMeshCompoundModalAnalysis))

    def results_for_cylindrical_gear_mesh(self, design_entity: '_1889.CylindricalGearMesh') -> 'Iterable[_4908.CylindricalGearMeshCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.CylindricalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.CylindricalGearMeshCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4908.CylindricalGearMeshCompoundModalAnalysis))

    def results_for_hypoid_gear_mesh(self, design_entity: '_1895.HypoidGearMesh') -> 'Iterable[_4922.HypoidGearMeshCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.HypoidGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.HypoidGearMeshCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4922.HypoidGearMeshCompoundModalAnalysis))

    def results_for_klingelnberg_cyclo_palloid_conical_gear_mesh(self, design_entity: '_1898.KlingelnbergCycloPalloidConicalGearMesh') -> 'Iterable[_4927.KlingelnbergCycloPalloidConicalGearMeshCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidConicalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.KlingelnbergCycloPalloidConicalGearMeshCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4927.KlingelnbergCycloPalloidConicalGearMeshCompoundModalAnalysis))

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_mesh(self, design_entity: '_1899.KlingelnbergCycloPalloidHypoidGearMesh') -> 'Iterable[_4930.KlingelnbergCycloPalloidHypoidGearMeshCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidHypoidGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.KlingelnbergCycloPalloidHypoidGearMeshCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4930.KlingelnbergCycloPalloidHypoidGearMeshCompoundModalAnalysis))

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(self, design_entity: '_1900.KlingelnbergCycloPalloidSpiralBevelGearMesh') -> 'Iterable[_4933.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidSpiralBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4933.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundModalAnalysis))

    def results_for_spiral_bevel_gear_mesh(self, design_entity: '_1903.SpiralBevelGearMesh') -> 'Iterable[_4958.SpiralBevelGearMeshCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.SpiralBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.SpiralBevelGearMeshCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4958.SpiralBevelGearMeshCompoundModalAnalysis))

    def results_for_straight_bevel_gear_mesh(self, design_entity: '_1907.StraightBevelGearMesh') -> 'Iterable[_4967.StraightBevelGearMeshCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.StraightBevelGearMeshCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4967.StraightBevelGearMeshCompoundModalAnalysis))

    def results_for_worm_gear_mesh(self, design_entity: '_1909.WormGearMesh') -> 'Iterable[_4982.WormGearMeshCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.WormGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.WormGearMeshCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4982.WormGearMeshCompoundModalAnalysis))

    def results_for_zerol_bevel_gear_mesh(self, design_entity: '_1911.ZerolBevelGearMesh') -> 'Iterable[_4985.ZerolBevelGearMeshCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ZerolBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.ZerolBevelGearMeshCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4985.ZerolBevelGearMeshCompoundModalAnalysis))

    def results_for_gear_mesh(self, design_entity: '_1893.GearMesh') -> 'Iterable[_4918.GearMeshCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.GearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.GearMeshCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4918.GearMeshCompoundModalAnalysis))

    def results_for_part_to_part_shear_coupling_connection(self, design_entity: '_1919.PartToPartShearCouplingConnection') -> 'Iterable[_4941.PartToPartShearCouplingConnectionCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.PartToPartShearCouplingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.PartToPartShearCouplingConnectionCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4941.PartToPartShearCouplingConnectionCompoundModalAnalysis))

    def results_for_clutch_connection(self, design_entity: '_1913.ClutchConnection') -> 'Iterable[_4886.ClutchConnectionCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ClutchConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.ClutchConnectionCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4886.ClutchConnectionCompoundModalAnalysis))

    def results_for_concept_coupling_connection(self, design_entity: '_1915.ConceptCouplingConnection') -> 'Iterable[_4891.ConceptCouplingConnectionCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ConceptCouplingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.ConceptCouplingConnectionCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4891.ConceptCouplingConnectionCompoundModalAnalysis))

    def results_for_coupling_connection(self, design_entity: '_1917.CouplingConnection') -> 'Iterable[_4902.CouplingConnectionCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.CouplingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.CouplingConnectionCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4902.CouplingConnectionCompoundModalAnalysis))

    def results_for_spring_damper_connection(self, design_entity: '_1921.SpringDamperConnection') -> 'Iterable[_4961.SpringDamperConnectionCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.SpringDamperConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.SpringDamperConnectionCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4961.SpringDamperConnectionCompoundModalAnalysis))

    def results_for_torque_converter_connection(self, design_entity: '_1923.TorqueConverterConnection') -> 'Iterable[_4976.TorqueConverterConnectionCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.TorqueConverterConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.TorqueConverterConnectionCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_4976.TorqueConverterConnectionCompoundModalAnalysis))
