'''_2222.py

CompoundSingleMeshWhineAnalysisAnalysis
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
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound import (
    _5555, _5556, _5561, _5572,
    _5573, _5578, _5589, _5600,
    _5601, _5605, _5560, _5609,
    _5613, _5624, _5625, _5626,
    _5627, _5628, _5634, _5635,
    _5636, _5641, _5645, _5668,
    _5669, _5642, _5582, _5584,
    _5602, _5604, _5557, _5559,
    _5564, _5566, _5567, _5568,
    _5569, _5571, _5585, _5587,
    _5596, _5598, _5599, _5606,
    _5608, _5610, _5612, _5615,
    _5617, _5618, _5620, _5621,
    _5623, _5633, _5646, _5648,
    _5652, _5654, _5655, _5657,
    _5658, _5659, _5670, _5672,
    _5673, _5675, _5629, _5631,
    _5563, _5574, _5576, _5579,
    _5581, _5590, _5592, _5594,
    _5595, _5637, _5643, _5639,
    _5638, _5649, _5651, _5660,
    _5661, _5662, _5663, _5664,
    _5666, _5667, _5593, _5562,
    _5577, _5588, _5614, _5632,
    _5640, _5644, _5565, _5583,
    _5603, _5653, _5570, _5586,
    _5558, _5597, _5611, _5616,
    _5619, _5622, _5647, _5656,
    _5671, _5674, _5607, _5630,
    _5575, _5580, _5591, _5650,
    _5665
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

_COMPOUND_SINGLE_MESH_WHINE_ANALYSIS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults', 'CompoundSingleMeshWhineAnalysisAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CompoundSingleMeshWhineAnalysisAnalysis',)


class CompoundSingleMeshWhineAnalysisAnalysis(_2173.CompoundAnalysis):
    '''CompoundSingleMeshWhineAnalysisAnalysis

    This is a mastapy class.
    '''

    TYPE = _COMPOUND_SINGLE_MESH_WHINE_ANALYSIS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CompoundSingleMeshWhineAnalysisAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    def results_for_abstract_assembly(self, design_entity: '_2000.AbstractAssembly') -> 'Iterable[_5555.AbstractAssemblyCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.AbstractAssemblyCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5555.AbstractAssemblyCompoundSingleMeshWhineAnalysis))

    def results_for_abstract_shaft_or_housing(self, design_entity: '_2001.AbstractShaftOrHousing') -> 'Iterable[_5556.AbstractShaftOrHousingCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractShaftOrHousing)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.AbstractShaftOrHousingCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5556.AbstractShaftOrHousingCompoundSingleMeshWhineAnalysis))

    def results_for_bearing(self, design_entity: '_2004.Bearing') -> 'Iterable[_5561.BearingCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bearing)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.BearingCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5561.BearingCompoundSingleMeshWhineAnalysis))

    def results_for_bolt(self, design_entity: '_2006.Bolt') -> 'Iterable[_5572.BoltCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bolt)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.BoltCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5572.BoltCompoundSingleMeshWhineAnalysis))

    def results_for_bolted_joint(self, design_entity: '_2007.BoltedJoint') -> 'Iterable[_5573.BoltedJointCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.BoltedJoint)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.BoltedJointCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5573.BoltedJointCompoundSingleMeshWhineAnalysis))

    def results_for_component(self, design_entity: '_2008.Component') -> 'Iterable[_5578.ComponentCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Component)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ComponentCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5578.ComponentCompoundSingleMeshWhineAnalysis))

    def results_for_connector(self, design_entity: '_2011.Connector') -> 'Iterable[_5589.ConnectorCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Connector)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ConnectorCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5589.ConnectorCompoundSingleMeshWhineAnalysis))

    def results_for_datum(self, design_entity: '_2012.Datum') -> 'Iterable[_5600.DatumCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Datum)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.DatumCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5600.DatumCompoundSingleMeshWhineAnalysis))

    def results_for_external_cad_model(self, design_entity: '_2015.ExternalCADModel') -> 'Iterable[_5601.ExternalCADModelCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ExternalCADModel)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ExternalCADModelCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5601.ExternalCADModelCompoundSingleMeshWhineAnalysis))

    def results_for_flexible_pin_assembly(self, design_entity: '_2016.FlexiblePinAssembly') -> 'Iterable[_5605.FlexiblePinAssemblyCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.FlexiblePinAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.FlexiblePinAssemblyCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5605.FlexiblePinAssemblyCompoundSingleMeshWhineAnalysis))

    def results_for_assembly(self, design_entity: '_1999.Assembly') -> 'Iterable[_5560.AssemblyCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Assembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.AssemblyCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5560.AssemblyCompoundSingleMeshWhineAnalysis))

    def results_for_guide_dxf_model(self, design_entity: '_2017.GuideDxfModel') -> 'Iterable[_5609.GuideDxfModelCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.GuideDxfModel)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.GuideDxfModelCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5609.GuideDxfModelCompoundSingleMeshWhineAnalysis))

    def results_for_imported_fe_component(self, design_entity: '_2020.ImportedFEComponent') -> 'Iterable[_5613.ImportedFEComponentCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ImportedFEComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ImportedFEComponentCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5613.ImportedFEComponentCompoundSingleMeshWhineAnalysis))

    def results_for_mass_disc(self, design_entity: '_2024.MassDisc') -> 'Iterable[_5624.MassDiscCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MassDisc)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.MassDiscCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5624.MassDiscCompoundSingleMeshWhineAnalysis))

    def results_for_measurement_component(self, design_entity: '_2025.MeasurementComponent') -> 'Iterable[_5625.MeasurementComponentCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MeasurementComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.MeasurementComponentCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5625.MeasurementComponentCompoundSingleMeshWhineAnalysis))

    def results_for_mountable_component(self, design_entity: '_2026.MountableComponent') -> 'Iterable[_5626.MountableComponentCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MountableComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.MountableComponentCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5626.MountableComponentCompoundSingleMeshWhineAnalysis))

    def results_for_oil_seal(self, design_entity: '_2028.OilSeal') -> 'Iterable[_5627.OilSealCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.OilSeal)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.OilSealCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5627.OilSealCompoundSingleMeshWhineAnalysis))

    def results_for_part(self, design_entity: '_2030.Part') -> 'Iterable[_5628.PartCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Part)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.PartCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5628.PartCompoundSingleMeshWhineAnalysis))

    def results_for_planet_carrier(self, design_entity: '_2031.PlanetCarrier') -> 'Iterable[_5634.PlanetCarrierCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PlanetCarrier)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.PlanetCarrierCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5634.PlanetCarrierCompoundSingleMeshWhineAnalysis))

    def results_for_point_load(self, design_entity: '_2033.PointLoad') -> 'Iterable[_5635.PointLoadCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PointLoad)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.PointLoadCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5635.PointLoadCompoundSingleMeshWhineAnalysis))

    def results_for_power_load(self, design_entity: '_2034.PowerLoad') -> 'Iterable[_5636.PowerLoadCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PowerLoad)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.PowerLoadCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5636.PowerLoadCompoundSingleMeshWhineAnalysis))

    def results_for_root_assembly(self, design_entity: '_2036.RootAssembly') -> 'Iterable[_5641.RootAssemblyCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.RootAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.RootAssemblyCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5641.RootAssemblyCompoundSingleMeshWhineAnalysis))

    def results_for_specialised_assembly(self, design_entity: '_2038.SpecialisedAssembly') -> 'Iterable[_5645.SpecialisedAssemblyCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.SpecialisedAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.SpecialisedAssemblyCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5645.SpecialisedAssemblyCompoundSingleMeshWhineAnalysis))

    def results_for_unbalanced_mass(self, design_entity: '_2039.UnbalancedMass') -> 'Iterable[_5668.UnbalancedMassCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.UnbalancedMass)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.UnbalancedMassCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5668.UnbalancedMassCompoundSingleMeshWhineAnalysis))

    def results_for_virtual_component(self, design_entity: '_2040.VirtualComponent') -> 'Iterable[_5669.VirtualComponentCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.VirtualComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.VirtualComponentCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5669.VirtualComponentCompoundSingleMeshWhineAnalysis))

    def results_for_shaft(self, design_entity: '_2043.Shaft') -> 'Iterable[_5642.ShaftCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.shaft_model.Shaft)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ShaftCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5642.ShaftCompoundSingleMeshWhineAnalysis))

    def results_for_concept_gear(self, design_entity: '_2081.ConceptGear') -> 'Iterable[_5582.ConceptGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ConceptGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5582.ConceptGearCompoundSingleMeshWhineAnalysis))

    def results_for_concept_gear_set(self, design_entity: '_2082.ConceptGearSet') -> 'Iterable[_5584.ConceptGearSetCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ConceptGearSetCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5584.ConceptGearSetCompoundSingleMeshWhineAnalysis))

    def results_for_face_gear(self, design_entity: '_2088.FaceGear') -> 'Iterable[_5602.FaceGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.FaceGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5602.FaceGearCompoundSingleMeshWhineAnalysis))

    def results_for_face_gear_set(self, design_entity: '_2089.FaceGearSet') -> 'Iterable[_5604.FaceGearSetCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.FaceGearSetCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5604.FaceGearSetCompoundSingleMeshWhineAnalysis))

    def results_for_agma_gleason_conical_gear(self, design_entity: '_2073.AGMAGleasonConicalGear') -> 'Iterable[_5557.AGMAGleasonConicalGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.AGMAGleasonConicalGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5557.AGMAGleasonConicalGearCompoundSingleMeshWhineAnalysis))

    def results_for_agma_gleason_conical_gear_set(self, design_entity: '_2074.AGMAGleasonConicalGearSet') -> 'Iterable[_5559.AGMAGleasonConicalGearSetCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.AGMAGleasonConicalGearSetCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5559.AGMAGleasonConicalGearSetCompoundSingleMeshWhineAnalysis))

    def results_for_bevel_differential_gear(self, design_entity: '_2075.BevelDifferentialGear') -> 'Iterable[_5564.BevelDifferentialGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.BevelDifferentialGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5564.BevelDifferentialGearCompoundSingleMeshWhineAnalysis))

    def results_for_bevel_differential_gear_set(self, design_entity: '_2076.BevelDifferentialGearSet') -> 'Iterable[_5566.BevelDifferentialGearSetCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.BevelDifferentialGearSetCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5566.BevelDifferentialGearSetCompoundSingleMeshWhineAnalysis))

    def results_for_bevel_differential_planet_gear(self, design_entity: '_2077.BevelDifferentialPlanetGear') -> 'Iterable[_5567.BevelDifferentialPlanetGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialPlanetGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.BevelDifferentialPlanetGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5567.BevelDifferentialPlanetGearCompoundSingleMeshWhineAnalysis))

    def results_for_bevel_differential_sun_gear(self, design_entity: '_2078.BevelDifferentialSunGear') -> 'Iterable[_5568.BevelDifferentialSunGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialSunGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.BevelDifferentialSunGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5568.BevelDifferentialSunGearCompoundSingleMeshWhineAnalysis))

    def results_for_bevel_gear(self, design_entity: '_2079.BevelGear') -> 'Iterable[_5569.BevelGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.BevelGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5569.BevelGearCompoundSingleMeshWhineAnalysis))

    def results_for_bevel_gear_set(self, design_entity: '_2080.BevelGearSet') -> 'Iterable[_5571.BevelGearSetCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.BevelGearSetCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5571.BevelGearSetCompoundSingleMeshWhineAnalysis))

    def results_for_conical_gear(self, design_entity: '_2083.ConicalGear') -> 'Iterable[_5585.ConicalGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ConicalGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5585.ConicalGearCompoundSingleMeshWhineAnalysis))

    def results_for_conical_gear_set(self, design_entity: '_2084.ConicalGearSet') -> 'Iterable[_5587.ConicalGearSetCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ConicalGearSetCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5587.ConicalGearSetCompoundSingleMeshWhineAnalysis))

    def results_for_cylindrical_gear(self, design_entity: '_2085.CylindricalGear') -> 'Iterable[_5596.CylindricalGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.CylindricalGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5596.CylindricalGearCompoundSingleMeshWhineAnalysis))

    def results_for_cylindrical_gear_set(self, design_entity: '_2086.CylindricalGearSet') -> 'Iterable[_5598.CylindricalGearSetCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.CylindricalGearSetCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5598.CylindricalGearSetCompoundSingleMeshWhineAnalysis))

    def results_for_cylindrical_planet_gear(self, design_entity: '_2087.CylindricalPlanetGear') -> 'Iterable[_5599.CylindricalPlanetGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalPlanetGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.CylindricalPlanetGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5599.CylindricalPlanetGearCompoundSingleMeshWhineAnalysis))

    def results_for_gear(self, design_entity: '_2090.Gear') -> 'Iterable[_5606.GearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.Gear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.GearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5606.GearCompoundSingleMeshWhineAnalysis))

    def results_for_gear_set(self, design_entity: '_2092.GearSet') -> 'Iterable[_5608.GearSetCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.GearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.GearSetCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5608.GearSetCompoundSingleMeshWhineAnalysis))

    def results_for_hypoid_gear(self, design_entity: '_2094.HypoidGear') -> 'Iterable[_5610.HypoidGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.HypoidGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5610.HypoidGearCompoundSingleMeshWhineAnalysis))

    def results_for_hypoid_gear_set(self, design_entity: '_2095.HypoidGearSet') -> 'Iterable[_5612.HypoidGearSetCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.HypoidGearSetCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5612.HypoidGearSetCompoundSingleMeshWhineAnalysis))

    def results_for_klingelnberg_cyclo_palloid_conical_gear(self, design_entity: '_2096.KlingelnbergCycloPalloidConicalGear') -> 'Iterable[_5615.KlingelnbergCycloPalloidConicalGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.KlingelnbergCycloPalloidConicalGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5615.KlingelnbergCycloPalloidConicalGearCompoundSingleMeshWhineAnalysis))

    def results_for_klingelnberg_cyclo_palloid_conical_gear_set(self, design_entity: '_2097.KlingelnbergCycloPalloidConicalGearSet') -> 'Iterable[_5617.KlingelnbergCycloPalloidConicalGearSetCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.KlingelnbergCycloPalloidConicalGearSetCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5617.KlingelnbergCycloPalloidConicalGearSetCompoundSingleMeshWhineAnalysis))

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear(self, design_entity: '_2098.KlingelnbergCycloPalloidHypoidGear') -> 'Iterable[_5618.KlingelnbergCycloPalloidHypoidGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.KlingelnbergCycloPalloidHypoidGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5618.KlingelnbergCycloPalloidHypoidGearCompoundSingleMeshWhineAnalysis))

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_set(self, design_entity: '_2099.KlingelnbergCycloPalloidHypoidGearSet') -> 'Iterable[_5620.KlingelnbergCycloPalloidHypoidGearSetCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.KlingelnbergCycloPalloidHypoidGearSetCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5620.KlingelnbergCycloPalloidHypoidGearSetCompoundSingleMeshWhineAnalysis))

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear(self, design_entity: '_2100.KlingelnbergCycloPalloidSpiralBevelGear') -> 'Iterable[_5621.KlingelnbergCycloPalloidSpiralBevelGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.KlingelnbergCycloPalloidSpiralBevelGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5621.KlingelnbergCycloPalloidSpiralBevelGearCompoundSingleMeshWhineAnalysis))

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self, design_entity: '_2101.KlingelnbergCycloPalloidSpiralBevelGearSet') -> 'Iterable[_5623.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5623.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSingleMeshWhineAnalysis))

    def results_for_planetary_gear_set(self, design_entity: '_2102.PlanetaryGearSet') -> 'Iterable[_5633.PlanetaryGearSetCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.PlanetaryGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.PlanetaryGearSetCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5633.PlanetaryGearSetCompoundSingleMeshWhineAnalysis))

    def results_for_spiral_bevel_gear(self, design_entity: '_2103.SpiralBevelGear') -> 'Iterable[_5646.SpiralBevelGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.SpiralBevelGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5646.SpiralBevelGearCompoundSingleMeshWhineAnalysis))

    def results_for_spiral_bevel_gear_set(self, design_entity: '_2104.SpiralBevelGearSet') -> 'Iterable[_5648.SpiralBevelGearSetCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.SpiralBevelGearSetCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5648.SpiralBevelGearSetCompoundSingleMeshWhineAnalysis))

    def results_for_straight_bevel_diff_gear(self, design_entity: '_2105.StraightBevelDiffGear') -> 'Iterable[_5652.StraightBevelDiffGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.StraightBevelDiffGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5652.StraightBevelDiffGearCompoundSingleMeshWhineAnalysis))

    def results_for_straight_bevel_diff_gear_set(self, design_entity: '_2106.StraightBevelDiffGearSet') -> 'Iterable[_5654.StraightBevelDiffGearSetCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.StraightBevelDiffGearSetCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5654.StraightBevelDiffGearSetCompoundSingleMeshWhineAnalysis))

    def results_for_straight_bevel_gear(self, design_entity: '_2107.StraightBevelGear') -> 'Iterable[_5655.StraightBevelGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.StraightBevelGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5655.StraightBevelGearCompoundSingleMeshWhineAnalysis))

    def results_for_straight_bevel_gear_set(self, design_entity: '_2108.StraightBevelGearSet') -> 'Iterable[_5657.StraightBevelGearSetCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.StraightBevelGearSetCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5657.StraightBevelGearSetCompoundSingleMeshWhineAnalysis))

    def results_for_straight_bevel_planet_gear(self, design_entity: '_2109.StraightBevelPlanetGear') -> 'Iterable[_5658.StraightBevelPlanetGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelPlanetGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.StraightBevelPlanetGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5658.StraightBevelPlanetGearCompoundSingleMeshWhineAnalysis))

    def results_for_straight_bevel_sun_gear(self, design_entity: '_2110.StraightBevelSunGear') -> 'Iterable[_5659.StraightBevelSunGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelSunGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.StraightBevelSunGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5659.StraightBevelSunGearCompoundSingleMeshWhineAnalysis))

    def results_for_worm_gear(self, design_entity: '_2111.WormGear') -> 'Iterable[_5670.WormGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.WormGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5670.WormGearCompoundSingleMeshWhineAnalysis))

    def results_for_worm_gear_set(self, design_entity: '_2112.WormGearSet') -> 'Iterable[_5672.WormGearSetCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.WormGearSetCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5672.WormGearSetCompoundSingleMeshWhineAnalysis))

    def results_for_zerol_bevel_gear(self, design_entity: '_2113.ZerolBevelGear') -> 'Iterable[_5673.ZerolBevelGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ZerolBevelGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5673.ZerolBevelGearCompoundSingleMeshWhineAnalysis))

    def results_for_zerol_bevel_gear_set(self, design_entity: '_2114.ZerolBevelGearSet') -> 'Iterable[_5675.ZerolBevelGearSetCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ZerolBevelGearSetCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5675.ZerolBevelGearSetCompoundSingleMeshWhineAnalysis))

    def results_for_part_to_part_shear_coupling(self, design_entity: '_2143.PartToPartShearCoupling') -> 'Iterable[_5629.PartToPartShearCouplingCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCoupling)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.PartToPartShearCouplingCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5629.PartToPartShearCouplingCompoundSingleMeshWhineAnalysis))

    def results_for_part_to_part_shear_coupling_half(self, design_entity: '_2144.PartToPartShearCouplingHalf') -> 'Iterable[_5631.PartToPartShearCouplingHalfCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCouplingHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.PartToPartShearCouplingHalfCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5631.PartToPartShearCouplingHalfCompoundSingleMeshWhineAnalysis))

    def results_for_belt_drive(self, design_entity: '_2132.BeltDrive') -> 'Iterable[_5563.BeltDriveCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.BeltDrive)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.BeltDriveCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5563.BeltDriveCompoundSingleMeshWhineAnalysis))

    def results_for_clutch(self, design_entity: '_2134.Clutch') -> 'Iterable[_5574.ClutchCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Clutch)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ClutchCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5574.ClutchCompoundSingleMeshWhineAnalysis))

    def results_for_clutch_half(self, design_entity: '_2135.ClutchHalf') -> 'Iterable[_5576.ClutchHalfCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ClutchHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ClutchHalfCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5576.ClutchHalfCompoundSingleMeshWhineAnalysis))

    def results_for_concept_coupling(self, design_entity: '_2137.ConceptCoupling') -> 'Iterable[_5579.ConceptCouplingCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCoupling)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ConceptCouplingCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5579.ConceptCouplingCompoundSingleMeshWhineAnalysis))

    def results_for_concept_coupling_half(self, design_entity: '_2138.ConceptCouplingHalf') -> 'Iterable[_5581.ConceptCouplingHalfCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCouplingHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ConceptCouplingHalfCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5581.ConceptCouplingHalfCompoundSingleMeshWhineAnalysis))

    def results_for_coupling(self, design_entity: '_2139.Coupling') -> 'Iterable[_5590.CouplingCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Coupling)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.CouplingCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5590.CouplingCompoundSingleMeshWhineAnalysis))

    def results_for_coupling_half(self, design_entity: '_2140.CouplingHalf') -> 'Iterable[_5592.CouplingHalfCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CouplingHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.CouplingHalfCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5592.CouplingHalfCompoundSingleMeshWhineAnalysis))

    def results_for_cvt(self, design_entity: '_2141.CVT') -> 'Iterable[_5594.CVTCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVT)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.CVTCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5594.CVTCompoundSingleMeshWhineAnalysis))

    def results_for_cvt_pulley(self, design_entity: '_2142.CVTPulley') -> 'Iterable[_5595.CVTPulleyCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVTPulley)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.CVTPulleyCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5595.CVTPulleyCompoundSingleMeshWhineAnalysis))

    def results_for_pulley(self, design_entity: '_2145.Pulley') -> 'Iterable[_5637.PulleyCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Pulley)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.PulleyCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5637.PulleyCompoundSingleMeshWhineAnalysis))

    def results_for_shaft_hub_connection(self, design_entity: '_2153.ShaftHubConnection') -> 'Iterable[_5643.ShaftHubConnectionCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ShaftHubConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ShaftHubConnectionCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5643.ShaftHubConnectionCompoundSingleMeshWhineAnalysis))

    def results_for_rolling_ring(self, design_entity: '_2151.RollingRing') -> 'Iterable[_5639.RollingRingCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRing)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.RollingRingCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5639.RollingRingCompoundSingleMeshWhineAnalysis))

    def results_for_rolling_ring_assembly(self, design_entity: '_2152.RollingRingAssembly') -> 'Iterable[_5638.RollingRingAssemblyCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRingAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.RollingRingAssemblyCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5638.RollingRingAssemblyCompoundSingleMeshWhineAnalysis))

    def results_for_spring_damper(self, design_entity: '_2154.SpringDamper') -> 'Iterable[_5649.SpringDamperCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamper)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.SpringDamperCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5649.SpringDamperCompoundSingleMeshWhineAnalysis))

    def results_for_spring_damper_half(self, design_entity: '_2155.SpringDamperHalf') -> 'Iterable[_5651.SpringDamperHalfCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamperHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.SpringDamperHalfCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5651.SpringDamperHalfCompoundSingleMeshWhineAnalysis))

    def results_for_synchroniser(self, design_entity: '_2156.Synchroniser') -> 'Iterable[_5660.SynchroniserCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Synchroniser)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.SynchroniserCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5660.SynchroniserCompoundSingleMeshWhineAnalysis))

    def results_for_synchroniser_half(self, design_entity: '_2158.SynchroniserHalf') -> 'Iterable[_5661.SynchroniserHalfCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.SynchroniserHalfCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5661.SynchroniserHalfCompoundSingleMeshWhineAnalysis))

    def results_for_synchroniser_part(self, design_entity: '_2159.SynchroniserPart') -> 'Iterable[_5662.SynchroniserPartCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserPart)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.SynchroniserPartCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5662.SynchroniserPartCompoundSingleMeshWhineAnalysis))

    def results_for_synchroniser_sleeve(self, design_entity: '_2160.SynchroniserSleeve') -> 'Iterable[_5663.SynchroniserSleeveCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserSleeve)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.SynchroniserSleeveCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5663.SynchroniserSleeveCompoundSingleMeshWhineAnalysis))

    def results_for_torque_converter(self, design_entity: '_2161.TorqueConverter') -> 'Iterable[_5664.TorqueConverterCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverter)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.TorqueConverterCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5664.TorqueConverterCompoundSingleMeshWhineAnalysis))

    def results_for_torque_converter_pump(self, design_entity: '_2162.TorqueConverterPump') -> 'Iterable[_5666.TorqueConverterPumpCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterPump)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.TorqueConverterPumpCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5666.TorqueConverterPumpCompoundSingleMeshWhineAnalysis))

    def results_for_torque_converter_turbine(self, design_entity: '_2164.TorqueConverterTurbine') -> 'Iterable[_5667.TorqueConverterTurbineCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterTurbine)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.TorqueConverterTurbineCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5667.TorqueConverterTurbineCompoundSingleMeshWhineAnalysis))

    def results_for_cvt_belt_connection(self, design_entity: '_1856.CVTBeltConnection') -> 'Iterable[_5593.CVTBeltConnectionCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CVTBeltConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.CVTBeltConnectionCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5593.CVTBeltConnectionCompoundSingleMeshWhineAnalysis))

    def results_for_belt_connection(self, design_entity: '_1851.BeltConnection') -> 'Iterable[_5562.BeltConnectionCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.BeltConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.BeltConnectionCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5562.BeltConnectionCompoundSingleMeshWhineAnalysis))

    def results_for_coaxial_connection(self, design_entity: '_1852.CoaxialConnection') -> 'Iterable[_5577.CoaxialConnectionCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CoaxialConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.CoaxialConnectionCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5577.CoaxialConnectionCompoundSingleMeshWhineAnalysis))

    def results_for_connection(self, design_entity: '_1855.Connection') -> 'Iterable[_5588.ConnectionCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.Connection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ConnectionCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5588.ConnectionCompoundSingleMeshWhineAnalysis))

    def results_for_inter_mountable_component_connection(self, design_entity: '_1864.InterMountableComponentConnection') -> 'Iterable[_5614.InterMountableComponentConnectionCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.InterMountableComponentConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.InterMountableComponentConnectionCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5614.InterMountableComponentConnectionCompoundSingleMeshWhineAnalysis))

    def results_for_planetary_connection(self, design_entity: '_1867.PlanetaryConnection') -> 'Iterable[_5632.PlanetaryConnectionCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.PlanetaryConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.PlanetaryConnectionCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5632.PlanetaryConnectionCompoundSingleMeshWhineAnalysis))

    def results_for_rolling_ring_connection(self, design_entity: '_1871.RollingRingConnection') -> 'Iterable[_5640.RollingRingConnectionCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.RollingRingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.RollingRingConnectionCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5640.RollingRingConnectionCompoundSingleMeshWhineAnalysis))

    def results_for_shaft_to_mountable_component_connection(self, design_entity: '_1875.ShaftToMountableComponentConnection') -> 'Iterable[_5644.ShaftToMountableComponentConnectionCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.ShaftToMountableComponentConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ShaftToMountableComponentConnectionCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5644.ShaftToMountableComponentConnectionCompoundSingleMeshWhineAnalysis))

    def results_for_bevel_differential_gear_mesh(self, design_entity: '_1881.BevelDifferentialGearMesh') -> 'Iterable[_5565.BevelDifferentialGearMeshCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelDifferentialGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.BevelDifferentialGearMeshCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5565.BevelDifferentialGearMeshCompoundSingleMeshWhineAnalysis))

    def results_for_concept_gear_mesh(self, design_entity: '_1885.ConceptGearMesh') -> 'Iterable[_5583.ConceptGearMeshCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConceptGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ConceptGearMeshCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5583.ConceptGearMeshCompoundSingleMeshWhineAnalysis))

    def results_for_face_gear_mesh(self, design_entity: '_1891.FaceGearMesh') -> 'Iterable[_5603.FaceGearMeshCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.FaceGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.FaceGearMeshCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5603.FaceGearMeshCompoundSingleMeshWhineAnalysis))

    def results_for_straight_bevel_diff_gear_mesh(self, design_entity: '_1905.StraightBevelDiffGearMesh') -> 'Iterable[_5653.StraightBevelDiffGearMeshCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelDiffGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.StraightBevelDiffGearMeshCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5653.StraightBevelDiffGearMeshCompoundSingleMeshWhineAnalysis))

    def results_for_bevel_gear_mesh(self, design_entity: '_1883.BevelGearMesh') -> 'Iterable[_5570.BevelGearMeshCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.BevelGearMeshCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5570.BevelGearMeshCompoundSingleMeshWhineAnalysis))

    def results_for_conical_gear_mesh(self, design_entity: '_1887.ConicalGearMesh') -> 'Iterable[_5586.ConicalGearMeshCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConicalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ConicalGearMeshCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5586.ConicalGearMeshCompoundSingleMeshWhineAnalysis))

    def results_for_agma_gleason_conical_gear_mesh(self, design_entity: '_1879.AGMAGleasonConicalGearMesh') -> 'Iterable[_5558.AGMAGleasonConicalGearMeshCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.AGMAGleasonConicalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.AGMAGleasonConicalGearMeshCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5558.AGMAGleasonConicalGearMeshCompoundSingleMeshWhineAnalysis))

    def results_for_cylindrical_gear_mesh(self, design_entity: '_1889.CylindricalGearMesh') -> 'Iterable[_5597.CylindricalGearMeshCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.CylindricalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.CylindricalGearMeshCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5597.CylindricalGearMeshCompoundSingleMeshWhineAnalysis))

    def results_for_hypoid_gear_mesh(self, design_entity: '_1895.HypoidGearMesh') -> 'Iterable[_5611.HypoidGearMeshCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.HypoidGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.HypoidGearMeshCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5611.HypoidGearMeshCompoundSingleMeshWhineAnalysis))

    def results_for_klingelnberg_cyclo_palloid_conical_gear_mesh(self, design_entity: '_1898.KlingelnbergCycloPalloidConicalGearMesh') -> 'Iterable[_5616.KlingelnbergCycloPalloidConicalGearMeshCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidConicalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.KlingelnbergCycloPalloidConicalGearMeshCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5616.KlingelnbergCycloPalloidConicalGearMeshCompoundSingleMeshWhineAnalysis))

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_mesh(self, design_entity: '_1899.KlingelnbergCycloPalloidHypoidGearMesh') -> 'Iterable[_5619.KlingelnbergCycloPalloidHypoidGearMeshCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidHypoidGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.KlingelnbergCycloPalloidHypoidGearMeshCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5619.KlingelnbergCycloPalloidHypoidGearMeshCompoundSingleMeshWhineAnalysis))

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(self, design_entity: '_1900.KlingelnbergCycloPalloidSpiralBevelGearMesh') -> 'Iterable[_5622.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidSpiralBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5622.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundSingleMeshWhineAnalysis))

    def results_for_spiral_bevel_gear_mesh(self, design_entity: '_1903.SpiralBevelGearMesh') -> 'Iterable[_5647.SpiralBevelGearMeshCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.SpiralBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.SpiralBevelGearMeshCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5647.SpiralBevelGearMeshCompoundSingleMeshWhineAnalysis))

    def results_for_straight_bevel_gear_mesh(self, design_entity: '_1907.StraightBevelGearMesh') -> 'Iterable[_5656.StraightBevelGearMeshCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.StraightBevelGearMeshCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5656.StraightBevelGearMeshCompoundSingleMeshWhineAnalysis))

    def results_for_worm_gear_mesh(self, design_entity: '_1909.WormGearMesh') -> 'Iterable[_5671.WormGearMeshCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.WormGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.WormGearMeshCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5671.WormGearMeshCompoundSingleMeshWhineAnalysis))

    def results_for_zerol_bevel_gear_mesh(self, design_entity: '_1911.ZerolBevelGearMesh') -> 'Iterable[_5674.ZerolBevelGearMeshCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ZerolBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ZerolBevelGearMeshCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5674.ZerolBevelGearMeshCompoundSingleMeshWhineAnalysis))

    def results_for_gear_mesh(self, design_entity: '_1893.GearMesh') -> 'Iterable[_5607.GearMeshCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.GearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.GearMeshCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5607.GearMeshCompoundSingleMeshWhineAnalysis))

    def results_for_part_to_part_shear_coupling_connection(self, design_entity: '_1919.PartToPartShearCouplingConnection') -> 'Iterable[_5630.PartToPartShearCouplingConnectionCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.PartToPartShearCouplingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.PartToPartShearCouplingConnectionCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5630.PartToPartShearCouplingConnectionCompoundSingleMeshWhineAnalysis))

    def results_for_clutch_connection(self, design_entity: '_1913.ClutchConnection') -> 'Iterable[_5575.ClutchConnectionCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ClutchConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ClutchConnectionCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5575.ClutchConnectionCompoundSingleMeshWhineAnalysis))

    def results_for_concept_coupling_connection(self, design_entity: '_1915.ConceptCouplingConnection') -> 'Iterable[_5580.ConceptCouplingConnectionCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ConceptCouplingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ConceptCouplingConnectionCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5580.ConceptCouplingConnectionCompoundSingleMeshWhineAnalysis))

    def results_for_coupling_connection(self, design_entity: '_1917.CouplingConnection') -> 'Iterable[_5591.CouplingConnectionCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.CouplingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.CouplingConnectionCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5591.CouplingConnectionCompoundSingleMeshWhineAnalysis))

    def results_for_spring_damper_connection(self, design_entity: '_1921.SpringDamperConnection') -> 'Iterable[_5650.SpringDamperConnectionCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.SpringDamperConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.SpringDamperConnectionCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5650.SpringDamperConnectionCompoundSingleMeshWhineAnalysis))

    def results_for_torque_converter_connection(self, design_entity: '_1923.TorqueConverterConnection') -> 'Iterable[_5665.TorqueConverterConnectionCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.TorqueConverterConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.TorqueConverterConnectionCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5665.TorqueConverterConnectionCompoundSingleMeshWhineAnalysis))
