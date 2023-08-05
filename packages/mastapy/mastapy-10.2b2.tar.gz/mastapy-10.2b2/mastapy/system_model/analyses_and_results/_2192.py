'''_2192.py

PowerFlowAnalysis
'''


from mastapy.system_model.analyses_and_results.static_loads import (
    _6235, _6236, _6238, _6182,
    _6181, _6080, _6093, _6092,
    _6098, _6097, _6111, _6110,
    _6113, _6114, _6191, _6197,
    _6195, _6193, _6207, _6206,
    _6218, _6217, _6219, _6220,
    _6224, _6225, _6226, _6112,
    _6079, _6094, _6107, _6162,
    _6183, _6194, _6199, _6082,
    _6100, _6138, _6210, _6087,
    _6104, _6074, _6117, _6158,
    _6164, _6167, _6170, _6203,
    _6213, _6234, _6237, _6144,
    _6180, _6091, _6096, _6109,
    _6205, _6223, _6070, _6071,
    _6078, _6090, _6089, _6095,
    _6108, _6123, _6136, _6140,
    _6077, _6148, _6160, _6172,
    _6173, _6175, _6177, _6179,
    _6186, _6189, _6190, _6196,
    _6200, _6231, _6232, _6198,
    _6099, _6101, _6137, _6139,
    _6073, _6075, _6081, _6083,
    _6084, _6085, _6086, _6088,
    _6102, _6106, _6115, _6119,
    _6120, _6142, _6147, _6157,
    _6159, _6163, _6165, _6166,
    _6168, _6169, _6171, _6184,
    _6202, _6204, _6209, _6211,
    _6212, _6214, _6215, _6216,
    _6233
)
from mastapy.system_model.analyses_and_results.power_flows import (
    _3359, _3361, _3362, _3315,
    _3314, _3246, _3259, _3258,
    _3264, _3263, _3275, _3274,
    _3277, _3278, _3323, _3328,
    _3326, _3324, _3337, _3336,
    _3348, _3346, _3347, _3349,
    _3352, _3353, _3354, _3276,
    _3245, _3260, _3271, _3298,
    _3316, _3325, _3330, _3247,
    _3265, _3286, _3338, _3252,
    _3268, _3240, _3280, _3294,
    _3299, _3302, _3305, _3332,
    _3341, _3357, _3360, _3290,
    _3313, _3257, _3262, _3273,
    _3335, _3351, _3238, _3239,
    _3244, _3256, _3255, _3261,
    _3272, _3284, _3285, _3289,
    _3243, _3293, _3297, _3308,
    _3309, _3310, _3311, _3312,
    _3318, _3319, _3322, _3327,
    _3331, _3355, _3356, _3329,
    _3266, _3267, _3287, _3288,
    _3241, _3242, _3248, _3249,
    _3250, _3251, _3253, _3254,
    _3269, _3270, _3281, _3282,
    _3283, _3291, _3292, _3295,
    _3296, _3300, _3301, _3303,
    _3304, _3306, _3307, _3317,
    _3333, _3334, _3339, _3340,
    _3342, _3343, _3344, _3345,
    _3358
)
from mastapy._internal import constructor
from mastapy.system_model.part_model.gears import (
    _2113, _2114, _2081, _2082,
    _2088, _2089, _2073, _2074,
    _2075, _2076, _2077, _2078,
    _2079, _2080, _2083, _2084,
    _2085, _2086, _2087, _2090,
    _2092, _2094, _2095, _2096,
    _2097, _2098, _2099, _2100,
    _2101, _2102, _2103, _2104,
    _2105, _2106, _2107, _2108,
    _2109, _2110, _2111, _2112
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
from mastapy.system_model.part_model import (
    _2000, _2001, _2004, _2006,
    _2007, _2008, _2011, _2012,
    _2015, _2016, _1999, _2017,
    _2020, _2024, _2025, _2026,
    _2028, _2030, _2031, _2033,
    _2034, _2036, _2038, _2039,
    _2040
)
from mastapy.system_model.part_model.shaft_model import _2043
from mastapy.system_model.analyses_and_results import _2174
from mastapy._internal.python_net import python_net_import

_POWER_FLOW_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults', 'PowerFlowAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PowerFlowAnalysis',)


class PowerFlowAnalysis(_2174.SingleAnalysis):
    '''PowerFlowAnalysis

    This is a mastapy class.
    '''

    TYPE = _POWER_FLOW_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PowerFlowAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    def results_for_worm_gear_set_load_case(self, design_entity_analysis: '_6235.WormGearSetLoadCase') -> '_3359.WormGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.WormGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.WormGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3359.WormGearSetPowerFlow)(method_result) if method_result else None

    def results_for_zerol_bevel_gear(self, design_entity: '_2113.ZerolBevelGear') -> '_3361.ZerolBevelGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ZerolBevelGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3361.ZerolBevelGearPowerFlow)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_load_case(self, design_entity_analysis: '_6236.ZerolBevelGearLoadCase') -> '_3361.ZerolBevelGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ZerolBevelGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3361.ZerolBevelGearPowerFlow)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_set(self, design_entity: '_2114.ZerolBevelGearSet') -> '_3362.ZerolBevelGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ZerolBevelGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3362.ZerolBevelGearSetPowerFlow)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_set_load_case(self, design_entity_analysis: '_6238.ZerolBevelGearSetLoadCase') -> '_3362.ZerolBevelGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ZerolBevelGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3362.ZerolBevelGearSetPowerFlow)(method_result) if method_result else None

    def results_for_part_to_part_shear_coupling(self, design_entity: '_2143.PartToPartShearCoupling') -> '_3315.PartToPartShearCouplingPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCoupling)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.PartToPartShearCouplingPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3315.PartToPartShearCouplingPowerFlow)(method_result) if method_result else None

    def results_for_part_to_part_shear_coupling_load_case(self, design_entity_analysis: '_6182.PartToPartShearCouplingLoadCase') -> '_3315.PartToPartShearCouplingPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PartToPartShearCouplingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.PartToPartShearCouplingPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3315.PartToPartShearCouplingPowerFlow)(method_result) if method_result else None

    def results_for_part_to_part_shear_coupling_half(self, design_entity: '_2144.PartToPartShearCouplingHalf') -> '_3314.PartToPartShearCouplingHalfPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCouplingHalf)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.PartToPartShearCouplingHalfPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3314.PartToPartShearCouplingHalfPowerFlow)(method_result) if method_result else None

    def results_for_part_to_part_shear_coupling_half_load_case(self, design_entity_analysis: '_6181.PartToPartShearCouplingHalfLoadCase') -> '_3314.PartToPartShearCouplingHalfPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PartToPartShearCouplingHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.PartToPartShearCouplingHalfPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3314.PartToPartShearCouplingHalfPowerFlow)(method_result) if method_result else None

    def results_for_belt_drive(self, design_entity: '_2132.BeltDrive') -> '_3246.BeltDrivePowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.BeltDrive)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BeltDrivePowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3246.BeltDrivePowerFlow)(method_result) if method_result else None

    def results_for_belt_drive_load_case(self, design_entity_analysis: '_6080.BeltDriveLoadCase') -> '_3246.BeltDrivePowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BeltDriveLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BeltDrivePowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3246.BeltDrivePowerFlow)(method_result) if method_result else None

    def results_for_clutch(self, design_entity: '_2134.Clutch') -> '_3259.ClutchPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Clutch)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ClutchPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3259.ClutchPowerFlow)(method_result) if method_result else None

    def results_for_clutch_load_case(self, design_entity_analysis: '_6093.ClutchLoadCase') -> '_3259.ClutchPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ClutchLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ClutchPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3259.ClutchPowerFlow)(method_result) if method_result else None

    def results_for_clutch_half(self, design_entity: '_2135.ClutchHalf') -> '_3258.ClutchHalfPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ClutchHalf)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ClutchHalfPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3258.ClutchHalfPowerFlow)(method_result) if method_result else None

    def results_for_clutch_half_load_case(self, design_entity_analysis: '_6092.ClutchHalfLoadCase') -> '_3258.ClutchHalfPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ClutchHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ClutchHalfPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3258.ClutchHalfPowerFlow)(method_result) if method_result else None

    def results_for_concept_coupling(self, design_entity: '_2137.ConceptCoupling') -> '_3264.ConceptCouplingPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCoupling)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ConceptCouplingPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3264.ConceptCouplingPowerFlow)(method_result) if method_result else None

    def results_for_concept_coupling_load_case(self, design_entity_analysis: '_6098.ConceptCouplingLoadCase') -> '_3264.ConceptCouplingPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ConceptCouplingPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3264.ConceptCouplingPowerFlow)(method_result) if method_result else None

    def results_for_concept_coupling_half(self, design_entity: '_2138.ConceptCouplingHalf') -> '_3263.ConceptCouplingHalfPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCouplingHalf)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ConceptCouplingHalfPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3263.ConceptCouplingHalfPowerFlow)(method_result) if method_result else None

    def results_for_concept_coupling_half_load_case(self, design_entity_analysis: '_6097.ConceptCouplingHalfLoadCase') -> '_3263.ConceptCouplingHalfPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ConceptCouplingHalfPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3263.ConceptCouplingHalfPowerFlow)(method_result) if method_result else None

    def results_for_coupling(self, design_entity: '_2139.Coupling') -> '_3275.CouplingPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Coupling)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.CouplingPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3275.CouplingPowerFlow)(method_result) if method_result else None

    def results_for_coupling_load_case(self, design_entity_analysis: '_6111.CouplingLoadCase') -> '_3275.CouplingPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CouplingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.CouplingPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3275.CouplingPowerFlow)(method_result) if method_result else None

    def results_for_coupling_half(self, design_entity: '_2140.CouplingHalf') -> '_3274.CouplingHalfPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CouplingHalf)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.CouplingHalfPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3274.CouplingHalfPowerFlow)(method_result) if method_result else None

    def results_for_coupling_half_load_case(self, design_entity_analysis: '_6110.CouplingHalfLoadCase') -> '_3274.CouplingHalfPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CouplingHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.CouplingHalfPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3274.CouplingHalfPowerFlow)(method_result) if method_result else None

    def results_for_cvt(self, design_entity: '_2141.CVT') -> '_3277.CVTPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVT)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.CVTPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3277.CVTPowerFlow)(method_result) if method_result else None

    def results_for_cvt_load_case(self, design_entity_analysis: '_6113.CVTLoadCase') -> '_3277.CVTPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CVTLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.CVTPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3277.CVTPowerFlow)(method_result) if method_result else None

    def results_for_cvt_pulley(self, design_entity: '_2142.CVTPulley') -> '_3278.CVTPulleyPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVTPulley)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.CVTPulleyPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3278.CVTPulleyPowerFlow)(method_result) if method_result else None

    def results_for_cvt_pulley_load_case(self, design_entity_analysis: '_6114.CVTPulleyLoadCase') -> '_3278.CVTPulleyPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CVTPulleyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.CVTPulleyPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3278.CVTPulleyPowerFlow)(method_result) if method_result else None

    def results_for_pulley(self, design_entity: '_2145.Pulley') -> '_3323.PulleyPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Pulley)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.PulleyPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3323.PulleyPowerFlow)(method_result) if method_result else None

    def results_for_pulley_load_case(self, design_entity_analysis: '_6191.PulleyLoadCase') -> '_3323.PulleyPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PulleyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.PulleyPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3323.PulleyPowerFlow)(method_result) if method_result else None

    def results_for_shaft_hub_connection(self, design_entity: '_2153.ShaftHubConnection') -> '_3328.ShaftHubConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ShaftHubConnection)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ShaftHubConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3328.ShaftHubConnectionPowerFlow)(method_result) if method_result else None

    def results_for_shaft_hub_connection_load_case(self, design_entity_analysis: '_6197.ShaftHubConnectionLoadCase') -> '_3328.ShaftHubConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ShaftHubConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ShaftHubConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3328.ShaftHubConnectionPowerFlow)(method_result) if method_result else None

    def results_for_rolling_ring(self, design_entity: '_2151.RollingRing') -> '_3326.RollingRingPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRing)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.RollingRingPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3326.RollingRingPowerFlow)(method_result) if method_result else None

    def results_for_rolling_ring_load_case(self, design_entity_analysis: '_6195.RollingRingLoadCase') -> '_3326.RollingRingPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RollingRingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.RollingRingPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3326.RollingRingPowerFlow)(method_result) if method_result else None

    def results_for_rolling_ring_assembly(self, design_entity: '_2152.RollingRingAssembly') -> '_3324.RollingRingAssemblyPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRingAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.RollingRingAssemblyPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3324.RollingRingAssemblyPowerFlow)(method_result) if method_result else None

    def results_for_rolling_ring_assembly_load_case(self, design_entity_analysis: '_6193.RollingRingAssemblyLoadCase') -> '_3324.RollingRingAssemblyPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RollingRingAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.RollingRingAssemblyPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3324.RollingRingAssemblyPowerFlow)(method_result) if method_result else None

    def results_for_spring_damper(self, design_entity: '_2154.SpringDamper') -> '_3337.SpringDamperPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamper)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.SpringDamperPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3337.SpringDamperPowerFlow)(method_result) if method_result else None

    def results_for_spring_damper_load_case(self, design_entity_analysis: '_6207.SpringDamperLoadCase') -> '_3337.SpringDamperPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpringDamperLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.SpringDamperPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3337.SpringDamperPowerFlow)(method_result) if method_result else None

    def results_for_spring_damper_half(self, design_entity: '_2155.SpringDamperHalf') -> '_3336.SpringDamperHalfPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamperHalf)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.SpringDamperHalfPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3336.SpringDamperHalfPowerFlow)(method_result) if method_result else None

    def results_for_spring_damper_half_load_case(self, design_entity_analysis: '_6206.SpringDamperHalfLoadCase') -> '_3336.SpringDamperHalfPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpringDamperHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.SpringDamperHalfPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3336.SpringDamperHalfPowerFlow)(method_result) if method_result else None

    def results_for_synchroniser(self, design_entity: '_2156.Synchroniser') -> '_3348.SynchroniserPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Synchroniser)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.SynchroniserPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3348.SynchroniserPowerFlow)(method_result) if method_result else None

    def results_for_synchroniser_load_case(self, design_entity_analysis: '_6218.SynchroniserLoadCase') -> '_3348.SynchroniserPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SynchroniserLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.SynchroniserPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3348.SynchroniserPowerFlow)(method_result) if method_result else None

    def results_for_synchroniser_half(self, design_entity: '_2158.SynchroniserHalf') -> '_3346.SynchroniserHalfPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserHalf)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.SynchroniserHalfPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3346.SynchroniserHalfPowerFlow)(method_result) if method_result else None

    def results_for_synchroniser_half_load_case(self, design_entity_analysis: '_6217.SynchroniserHalfLoadCase') -> '_3346.SynchroniserHalfPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SynchroniserHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.SynchroniserHalfPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3346.SynchroniserHalfPowerFlow)(method_result) if method_result else None

    def results_for_synchroniser_part(self, design_entity: '_2159.SynchroniserPart') -> '_3347.SynchroniserPartPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserPart)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.SynchroniserPartPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3347.SynchroniserPartPowerFlow)(method_result) if method_result else None

    def results_for_synchroniser_part_load_case(self, design_entity_analysis: '_6219.SynchroniserPartLoadCase') -> '_3347.SynchroniserPartPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SynchroniserPartLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.SynchroniserPartPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3347.SynchroniserPartPowerFlow)(method_result) if method_result else None

    def results_for_synchroniser_sleeve(self, design_entity: '_2160.SynchroniserSleeve') -> '_3349.SynchroniserSleevePowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserSleeve)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.SynchroniserSleevePowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3349.SynchroniserSleevePowerFlow)(method_result) if method_result else None

    def results_for_synchroniser_sleeve_load_case(self, design_entity_analysis: '_6220.SynchroniserSleeveLoadCase') -> '_3349.SynchroniserSleevePowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SynchroniserSleeveLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.SynchroniserSleevePowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3349.SynchroniserSleevePowerFlow)(method_result) if method_result else None

    def results_for_torque_converter(self, design_entity: '_2161.TorqueConverter') -> '_3352.TorqueConverterPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverter)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.TorqueConverterPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3352.TorqueConverterPowerFlow)(method_result) if method_result else None

    def results_for_torque_converter_load_case(self, design_entity_analysis: '_6224.TorqueConverterLoadCase') -> '_3352.TorqueConverterPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.TorqueConverterLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.TorqueConverterPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3352.TorqueConverterPowerFlow)(method_result) if method_result else None

    def results_for_torque_converter_pump(self, design_entity: '_2162.TorqueConverterPump') -> '_3353.TorqueConverterPumpPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterPump)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.TorqueConverterPumpPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3353.TorqueConverterPumpPowerFlow)(method_result) if method_result else None

    def results_for_torque_converter_pump_load_case(self, design_entity_analysis: '_6225.TorqueConverterPumpLoadCase') -> '_3353.TorqueConverterPumpPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.TorqueConverterPumpLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.TorqueConverterPumpPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3353.TorqueConverterPumpPowerFlow)(method_result) if method_result else None

    def results_for_torque_converter_turbine(self, design_entity: '_2164.TorqueConverterTurbine') -> '_3354.TorqueConverterTurbinePowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterTurbine)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.TorqueConverterTurbinePowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3354.TorqueConverterTurbinePowerFlow)(method_result) if method_result else None

    def results_for_torque_converter_turbine_load_case(self, design_entity_analysis: '_6226.TorqueConverterTurbineLoadCase') -> '_3354.TorqueConverterTurbinePowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.TorqueConverterTurbineLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.TorqueConverterTurbinePowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3354.TorqueConverterTurbinePowerFlow)(method_result) if method_result else None

    def results_for_cvt_belt_connection(self, design_entity: '_1856.CVTBeltConnection') -> '_3276.CVTBeltConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CVTBeltConnection)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.CVTBeltConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3276.CVTBeltConnectionPowerFlow)(method_result) if method_result else None

    def results_for_cvt_belt_connection_load_case(self, design_entity_analysis: '_6112.CVTBeltConnectionLoadCase') -> '_3276.CVTBeltConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CVTBeltConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.CVTBeltConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3276.CVTBeltConnectionPowerFlow)(method_result) if method_result else None

    def results_for_belt_connection(self, design_entity: '_1851.BeltConnection') -> '_3245.BeltConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.BeltConnection)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BeltConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3245.BeltConnectionPowerFlow)(method_result) if method_result else None

    def results_for_belt_connection_load_case(self, design_entity_analysis: '_6079.BeltConnectionLoadCase') -> '_3245.BeltConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BeltConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BeltConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3245.BeltConnectionPowerFlow)(method_result) if method_result else None

    def results_for_coaxial_connection(self, design_entity: '_1852.CoaxialConnection') -> '_3260.CoaxialConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CoaxialConnection)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.CoaxialConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3260.CoaxialConnectionPowerFlow)(method_result) if method_result else None

    def results_for_coaxial_connection_load_case(self, design_entity_analysis: '_6094.CoaxialConnectionLoadCase') -> '_3260.CoaxialConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CoaxialConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.CoaxialConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3260.CoaxialConnectionPowerFlow)(method_result) if method_result else None

    def results_for_connection(self, design_entity: '_1855.Connection') -> '_3271.ConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.Connection)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3271.ConnectionPowerFlow)(method_result) if method_result else None

    def results_for_connection_load_case(self, design_entity_analysis: '_6107.ConnectionLoadCase') -> '_3271.ConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3271.ConnectionPowerFlow)(method_result) if method_result else None

    def results_for_inter_mountable_component_connection(self, design_entity: '_1864.InterMountableComponentConnection') -> '_3298.InterMountableComponentConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.InterMountableComponentConnection)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.InterMountableComponentConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3298.InterMountableComponentConnectionPowerFlow)(method_result) if method_result else None

    def results_for_inter_mountable_component_connection_load_case(self, design_entity_analysis: '_6162.InterMountableComponentConnectionLoadCase') -> '_3298.InterMountableComponentConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.InterMountableComponentConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.InterMountableComponentConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3298.InterMountableComponentConnectionPowerFlow)(method_result) if method_result else None

    def results_for_planetary_connection(self, design_entity: '_1867.PlanetaryConnection') -> '_3316.PlanetaryConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.PlanetaryConnection)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.PlanetaryConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3316.PlanetaryConnectionPowerFlow)(method_result) if method_result else None

    def results_for_planetary_connection_load_case(self, design_entity_analysis: '_6183.PlanetaryConnectionLoadCase') -> '_3316.PlanetaryConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PlanetaryConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.PlanetaryConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3316.PlanetaryConnectionPowerFlow)(method_result) if method_result else None

    def results_for_rolling_ring_connection(self, design_entity: '_1871.RollingRingConnection') -> '_3325.RollingRingConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.RollingRingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.RollingRingConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3325.RollingRingConnectionPowerFlow)(method_result) if method_result else None

    def results_for_rolling_ring_connection_load_case(self, design_entity_analysis: '_6194.RollingRingConnectionLoadCase') -> '_3325.RollingRingConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RollingRingConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.RollingRingConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3325.RollingRingConnectionPowerFlow)(method_result) if method_result else None

    def results_for_shaft_to_mountable_component_connection(self, design_entity: '_1875.ShaftToMountableComponentConnection') -> '_3330.ShaftToMountableComponentConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.ShaftToMountableComponentConnection)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ShaftToMountableComponentConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3330.ShaftToMountableComponentConnectionPowerFlow)(method_result) if method_result else None

    def results_for_shaft_to_mountable_component_connection_load_case(self, design_entity_analysis: '_6199.ShaftToMountableComponentConnectionLoadCase') -> '_3330.ShaftToMountableComponentConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ShaftToMountableComponentConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ShaftToMountableComponentConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3330.ShaftToMountableComponentConnectionPowerFlow)(method_result) if method_result else None

    def results_for_bevel_differential_gear_mesh(self, design_entity: '_1881.BevelDifferentialGearMesh') -> '_3247.BevelDifferentialGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelDifferentialGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BevelDifferentialGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3247.BevelDifferentialGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_bevel_differential_gear_mesh_load_case(self, design_entity_analysis: '_6082.BevelDifferentialGearMeshLoadCase') -> '_3247.BevelDifferentialGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BevelDifferentialGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3247.BevelDifferentialGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_concept_gear_mesh(self, design_entity: '_1885.ConceptGearMesh') -> '_3265.ConceptGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConceptGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ConceptGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3265.ConceptGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_concept_gear_mesh_load_case(self, design_entity_analysis: '_6100.ConceptGearMeshLoadCase') -> '_3265.ConceptGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ConceptGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3265.ConceptGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_face_gear_mesh(self, design_entity: '_1891.FaceGearMesh') -> '_3286.FaceGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.FaceGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.FaceGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3286.FaceGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_face_gear_mesh_load_case(self, design_entity_analysis: '_6138.FaceGearMeshLoadCase') -> '_3286.FaceGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FaceGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.FaceGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3286.FaceGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_mesh(self, design_entity: '_1905.StraightBevelDiffGearMesh') -> '_3338.StraightBevelDiffGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelDiffGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.StraightBevelDiffGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3338.StraightBevelDiffGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_mesh_load_case(self, design_entity_analysis: '_6210.StraightBevelDiffGearMeshLoadCase') -> '_3338.StraightBevelDiffGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.StraightBevelDiffGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3338.StraightBevelDiffGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_bevel_gear_mesh(self, design_entity: '_1883.BevelGearMesh') -> '_3252.BevelGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BevelGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3252.BevelGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_bevel_gear_mesh_load_case(self, design_entity_analysis: '_6087.BevelGearMeshLoadCase') -> '_3252.BevelGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BevelGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3252.BevelGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_conical_gear_mesh(self, design_entity: '_1887.ConicalGearMesh') -> '_3268.ConicalGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConicalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ConicalGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3268.ConicalGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_conical_gear_mesh_load_case(self, design_entity_analysis: '_6104.ConicalGearMeshLoadCase') -> '_3268.ConicalGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConicalGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ConicalGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3268.ConicalGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_mesh(self, design_entity: '_1879.AGMAGleasonConicalGearMesh') -> '_3240.AGMAGleasonConicalGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.AGMAGleasonConicalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.AGMAGleasonConicalGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3240.AGMAGleasonConicalGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_mesh_load_case(self, design_entity_analysis: '_6074.AGMAGleasonConicalGearMeshLoadCase') -> '_3240.AGMAGleasonConicalGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.AGMAGleasonConicalGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3240.AGMAGleasonConicalGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_cylindrical_gear_mesh(self, design_entity: '_1889.CylindricalGearMesh') -> '_3280.CylindricalGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.CylindricalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.CylindricalGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3280.CylindricalGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_cylindrical_gear_mesh_load_case(self, design_entity_analysis: '_6117.CylindricalGearMeshLoadCase') -> '_3280.CylindricalGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CylindricalGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.CylindricalGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3280.CylindricalGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_hypoid_gear_mesh(self, design_entity: '_1895.HypoidGearMesh') -> '_3294.HypoidGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.HypoidGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.HypoidGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3294.HypoidGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_hypoid_gear_mesh_load_case(self, design_entity_analysis: '_6158.HypoidGearMeshLoadCase') -> '_3294.HypoidGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.HypoidGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.HypoidGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3294.HypoidGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_mesh(self, design_entity: '_1898.KlingelnbergCycloPalloidConicalGearMesh') -> '_3299.KlingelnbergCycloPalloidConicalGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidConicalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.KlingelnbergCycloPalloidConicalGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3299.KlingelnbergCycloPalloidConicalGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_mesh_load_case(self, design_entity_analysis: '_6164.KlingelnbergCycloPalloidConicalGearMeshLoadCase') -> '_3299.KlingelnbergCycloPalloidConicalGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.KlingelnbergCycloPalloidConicalGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3299.KlingelnbergCycloPalloidConicalGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_mesh(self, design_entity: '_1899.KlingelnbergCycloPalloidHypoidGearMesh') -> '_3302.KlingelnbergCycloPalloidHypoidGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidHypoidGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.KlingelnbergCycloPalloidHypoidGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3302.KlingelnbergCycloPalloidHypoidGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_mesh_load_case(self, design_entity_analysis: '_6167.KlingelnbergCycloPalloidHypoidGearMeshLoadCase') -> '_3302.KlingelnbergCycloPalloidHypoidGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.KlingelnbergCycloPalloidHypoidGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3302.KlingelnbergCycloPalloidHypoidGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(self, design_entity: '_1900.KlingelnbergCycloPalloidSpiralBevelGearMesh') -> '_3305.KlingelnbergCycloPalloidSpiralBevelGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidSpiralBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.KlingelnbergCycloPalloidSpiralBevelGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3305.KlingelnbergCycloPalloidSpiralBevelGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_load_case(self, design_entity_analysis: '_6170.KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase') -> '_3305.KlingelnbergCycloPalloidSpiralBevelGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.KlingelnbergCycloPalloidSpiralBevelGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3305.KlingelnbergCycloPalloidSpiralBevelGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_mesh(self, design_entity: '_1903.SpiralBevelGearMesh') -> '_3332.SpiralBevelGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.SpiralBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.SpiralBevelGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3332.SpiralBevelGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_mesh_load_case(self, design_entity_analysis: '_6203.SpiralBevelGearMeshLoadCase') -> '_3332.SpiralBevelGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.SpiralBevelGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3332.SpiralBevelGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_straight_bevel_gear_mesh(self, design_entity: '_1907.StraightBevelGearMesh') -> '_3341.StraightBevelGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.StraightBevelGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3341.StraightBevelGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_straight_bevel_gear_mesh_load_case(self, design_entity_analysis: '_6213.StraightBevelGearMeshLoadCase') -> '_3341.StraightBevelGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.StraightBevelGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3341.StraightBevelGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_worm_gear_mesh(self, design_entity: '_1909.WormGearMesh') -> '_3357.WormGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.WormGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.WormGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3357.WormGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_worm_gear_mesh_load_case(self, design_entity_analysis: '_6234.WormGearMeshLoadCase') -> '_3357.WormGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.WormGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.WormGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3357.WormGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_mesh(self, design_entity: '_1911.ZerolBevelGearMesh') -> '_3360.ZerolBevelGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ZerolBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ZerolBevelGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3360.ZerolBevelGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_mesh_load_case(self, design_entity_analysis: '_6237.ZerolBevelGearMeshLoadCase') -> '_3360.ZerolBevelGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ZerolBevelGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3360.ZerolBevelGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_gear_mesh(self, design_entity: '_1893.GearMesh') -> '_3290.GearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.GearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.GearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3290.GearMeshPowerFlow)(method_result) if method_result else None

    def results_for_gear_mesh_load_case(self, design_entity_analysis: '_6144.GearMeshLoadCase') -> '_3290.GearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.GearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.GearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3290.GearMeshPowerFlow)(method_result) if method_result else None

    def results_for_part_to_part_shear_coupling_connection(self, design_entity: '_1919.PartToPartShearCouplingConnection') -> '_3313.PartToPartShearCouplingConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.PartToPartShearCouplingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.PartToPartShearCouplingConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3313.PartToPartShearCouplingConnectionPowerFlow)(method_result) if method_result else None

    def results_for_part_to_part_shear_coupling_connection_load_case(self, design_entity_analysis: '_6180.PartToPartShearCouplingConnectionLoadCase') -> '_3313.PartToPartShearCouplingConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PartToPartShearCouplingConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.PartToPartShearCouplingConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3313.PartToPartShearCouplingConnectionPowerFlow)(method_result) if method_result else None

    def results_for_clutch_connection(self, design_entity: '_1913.ClutchConnection') -> '_3257.ClutchConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ClutchConnection)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ClutchConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3257.ClutchConnectionPowerFlow)(method_result) if method_result else None

    def results_for_clutch_connection_load_case(self, design_entity_analysis: '_6091.ClutchConnectionLoadCase') -> '_3257.ClutchConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ClutchConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ClutchConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3257.ClutchConnectionPowerFlow)(method_result) if method_result else None

    def results_for_concept_coupling_connection(self, design_entity: '_1915.ConceptCouplingConnection') -> '_3262.ConceptCouplingConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ConceptCouplingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ConceptCouplingConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3262.ConceptCouplingConnectionPowerFlow)(method_result) if method_result else None

    def results_for_concept_coupling_connection_load_case(self, design_entity_analysis: '_6096.ConceptCouplingConnectionLoadCase') -> '_3262.ConceptCouplingConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ConceptCouplingConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3262.ConceptCouplingConnectionPowerFlow)(method_result) if method_result else None

    def results_for_coupling_connection(self, design_entity: '_1917.CouplingConnection') -> '_3273.CouplingConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.CouplingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.CouplingConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3273.CouplingConnectionPowerFlow)(method_result) if method_result else None

    def results_for_coupling_connection_load_case(self, design_entity_analysis: '_6109.CouplingConnectionLoadCase') -> '_3273.CouplingConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CouplingConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.CouplingConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3273.CouplingConnectionPowerFlow)(method_result) if method_result else None

    def results_for_spring_damper_connection(self, design_entity: '_1921.SpringDamperConnection') -> '_3335.SpringDamperConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.SpringDamperConnection)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.SpringDamperConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3335.SpringDamperConnectionPowerFlow)(method_result) if method_result else None

    def results_for_spring_damper_connection_load_case(self, design_entity_analysis: '_6205.SpringDamperConnectionLoadCase') -> '_3335.SpringDamperConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpringDamperConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.SpringDamperConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3335.SpringDamperConnectionPowerFlow)(method_result) if method_result else None

    def results_for_torque_converter_connection(self, design_entity: '_1923.TorqueConverterConnection') -> '_3351.TorqueConverterConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.TorqueConverterConnection)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.TorqueConverterConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3351.TorqueConverterConnectionPowerFlow)(method_result) if method_result else None

    def results_for_torque_converter_connection_load_case(self, design_entity_analysis: '_6223.TorqueConverterConnectionLoadCase') -> '_3351.TorqueConverterConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.TorqueConverterConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.TorqueConverterConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3351.TorqueConverterConnectionPowerFlow)(method_result) if method_result else None

    def results_for_abstract_assembly(self, design_entity: '_2000.AbstractAssembly') -> '_3238.AbstractAssemblyPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.AbstractAssemblyPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3238.AbstractAssemblyPowerFlow)(method_result) if method_result else None

    def results_for_abstract_assembly_load_case(self, design_entity_analysis: '_6070.AbstractAssemblyLoadCase') -> '_3238.AbstractAssemblyPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AbstractAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.AbstractAssemblyPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3238.AbstractAssemblyPowerFlow)(method_result) if method_result else None

    def results_for_abstract_shaft_or_housing(self, design_entity: '_2001.AbstractShaftOrHousing') -> '_3239.AbstractShaftOrHousingPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractShaftOrHousing)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.AbstractShaftOrHousingPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3239.AbstractShaftOrHousingPowerFlow)(method_result) if method_result else None

    def results_for_abstract_shaft_or_housing_load_case(self, design_entity_analysis: '_6071.AbstractShaftOrHousingLoadCase') -> '_3239.AbstractShaftOrHousingPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AbstractShaftOrHousingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.AbstractShaftOrHousingPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3239.AbstractShaftOrHousingPowerFlow)(method_result) if method_result else None

    def results_for_bearing(self, design_entity: '_2004.Bearing') -> '_3244.BearingPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bearing)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BearingPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3244.BearingPowerFlow)(method_result) if method_result else None

    def results_for_bearing_load_case(self, design_entity_analysis: '_6078.BearingLoadCase') -> '_3244.BearingPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BearingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BearingPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3244.BearingPowerFlow)(method_result) if method_result else None

    def results_for_bolt(self, design_entity: '_2006.Bolt') -> '_3256.BoltPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bolt)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BoltPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3256.BoltPowerFlow)(method_result) if method_result else None

    def results_for_bolt_load_case(self, design_entity_analysis: '_6090.BoltLoadCase') -> '_3256.BoltPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BoltLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BoltPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3256.BoltPowerFlow)(method_result) if method_result else None

    def results_for_bolted_joint(self, design_entity: '_2007.BoltedJoint') -> '_3255.BoltedJointPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.BoltedJoint)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BoltedJointPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3255.BoltedJointPowerFlow)(method_result) if method_result else None

    def results_for_bolted_joint_load_case(self, design_entity_analysis: '_6089.BoltedJointLoadCase') -> '_3255.BoltedJointPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BoltedJointLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BoltedJointPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3255.BoltedJointPowerFlow)(method_result) if method_result else None

    def results_for_component(self, design_entity: '_2008.Component') -> '_3261.ComponentPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Component)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ComponentPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3261.ComponentPowerFlow)(method_result) if method_result else None

    def results_for_component_load_case(self, design_entity_analysis: '_6095.ComponentLoadCase') -> '_3261.ComponentPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ComponentPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3261.ComponentPowerFlow)(method_result) if method_result else None

    def results_for_connector(self, design_entity: '_2011.Connector') -> '_3272.ConnectorPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Connector)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ConnectorPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3272.ConnectorPowerFlow)(method_result) if method_result else None

    def results_for_connector_load_case(self, design_entity_analysis: '_6108.ConnectorLoadCase') -> '_3272.ConnectorPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConnectorLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ConnectorPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3272.ConnectorPowerFlow)(method_result) if method_result else None

    def results_for_datum(self, design_entity: '_2012.Datum') -> '_3284.DatumPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Datum)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.DatumPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3284.DatumPowerFlow)(method_result) if method_result else None

    def results_for_datum_load_case(self, design_entity_analysis: '_6123.DatumLoadCase') -> '_3284.DatumPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.DatumLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.DatumPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3284.DatumPowerFlow)(method_result) if method_result else None

    def results_for_external_cad_model(self, design_entity: '_2015.ExternalCADModel') -> '_3285.ExternalCADModelPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ExternalCADModel)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ExternalCADModelPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3285.ExternalCADModelPowerFlow)(method_result) if method_result else None

    def results_for_external_cad_model_load_case(self, design_entity_analysis: '_6136.ExternalCADModelLoadCase') -> '_3285.ExternalCADModelPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ExternalCADModelLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ExternalCADModelPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3285.ExternalCADModelPowerFlow)(method_result) if method_result else None

    def results_for_flexible_pin_assembly(self, design_entity: '_2016.FlexiblePinAssembly') -> '_3289.FlexiblePinAssemblyPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.FlexiblePinAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.FlexiblePinAssemblyPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3289.FlexiblePinAssemblyPowerFlow)(method_result) if method_result else None

    def results_for_flexible_pin_assembly_load_case(self, design_entity_analysis: '_6140.FlexiblePinAssemblyLoadCase') -> '_3289.FlexiblePinAssemblyPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FlexiblePinAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.FlexiblePinAssemblyPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3289.FlexiblePinAssemblyPowerFlow)(method_result) if method_result else None

    def results_for_assembly(self, design_entity: '_1999.Assembly') -> '_3243.AssemblyPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Assembly)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.AssemblyPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3243.AssemblyPowerFlow)(method_result) if method_result else None

    def results_for_assembly_load_case(self, design_entity_analysis: '_6077.AssemblyLoadCase') -> '_3243.AssemblyPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.AssemblyPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3243.AssemblyPowerFlow)(method_result) if method_result else None

    def results_for_guide_dxf_model(self, design_entity: '_2017.GuideDxfModel') -> '_3293.GuideDxfModelPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.GuideDxfModel)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.GuideDxfModelPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3293.GuideDxfModelPowerFlow)(method_result) if method_result else None

    def results_for_guide_dxf_model_load_case(self, design_entity_analysis: '_6148.GuideDxfModelLoadCase') -> '_3293.GuideDxfModelPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.GuideDxfModelLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.GuideDxfModelPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3293.GuideDxfModelPowerFlow)(method_result) if method_result else None

    def results_for_imported_fe_component(self, design_entity: '_2020.ImportedFEComponent') -> '_3297.ImportedFEComponentPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ImportedFEComponent)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ImportedFEComponentPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3297.ImportedFEComponentPowerFlow)(method_result) if method_result else None

    def results_for_imported_fe_component_load_case(self, design_entity_analysis: '_6160.ImportedFEComponentLoadCase') -> '_3297.ImportedFEComponentPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ImportedFEComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ImportedFEComponentPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3297.ImportedFEComponentPowerFlow)(method_result) if method_result else None

    def results_for_mass_disc(self, design_entity: '_2024.MassDisc') -> '_3308.MassDiscPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MassDisc)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.MassDiscPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3308.MassDiscPowerFlow)(method_result) if method_result else None

    def results_for_mass_disc_load_case(self, design_entity_analysis: '_6172.MassDiscLoadCase') -> '_3308.MassDiscPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.MassDiscLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.MassDiscPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3308.MassDiscPowerFlow)(method_result) if method_result else None

    def results_for_measurement_component(self, design_entity: '_2025.MeasurementComponent') -> '_3309.MeasurementComponentPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MeasurementComponent)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.MeasurementComponentPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3309.MeasurementComponentPowerFlow)(method_result) if method_result else None

    def results_for_measurement_component_load_case(self, design_entity_analysis: '_6173.MeasurementComponentLoadCase') -> '_3309.MeasurementComponentPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.MeasurementComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.MeasurementComponentPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3309.MeasurementComponentPowerFlow)(method_result) if method_result else None

    def results_for_mountable_component(self, design_entity: '_2026.MountableComponent') -> '_3310.MountableComponentPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MountableComponent)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.MountableComponentPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3310.MountableComponentPowerFlow)(method_result) if method_result else None

    def results_for_mountable_component_load_case(self, design_entity_analysis: '_6175.MountableComponentLoadCase') -> '_3310.MountableComponentPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.MountableComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.MountableComponentPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3310.MountableComponentPowerFlow)(method_result) if method_result else None

    def results_for_oil_seal(self, design_entity: '_2028.OilSeal') -> '_3311.OilSealPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.OilSeal)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.OilSealPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3311.OilSealPowerFlow)(method_result) if method_result else None

    def results_for_oil_seal_load_case(self, design_entity_analysis: '_6177.OilSealLoadCase') -> '_3311.OilSealPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.OilSealLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.OilSealPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3311.OilSealPowerFlow)(method_result) if method_result else None

    def results_for_part(self, design_entity: '_2030.Part') -> '_3312.PartPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Part)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.PartPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3312.PartPowerFlow)(method_result) if method_result else None

    def results_for_part_load_case(self, design_entity_analysis: '_6179.PartLoadCase') -> '_3312.PartPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PartLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.PartPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3312.PartPowerFlow)(method_result) if method_result else None

    def results_for_planet_carrier(self, design_entity: '_2031.PlanetCarrier') -> '_3318.PlanetCarrierPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PlanetCarrier)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.PlanetCarrierPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3318.PlanetCarrierPowerFlow)(method_result) if method_result else None

    def results_for_planet_carrier_load_case(self, design_entity_analysis: '_6186.PlanetCarrierLoadCase') -> '_3318.PlanetCarrierPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PlanetCarrierLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.PlanetCarrierPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3318.PlanetCarrierPowerFlow)(method_result) if method_result else None

    def results_for_point_load(self, design_entity: '_2033.PointLoad') -> '_3319.PointLoadPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PointLoad)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.PointLoadPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3319.PointLoadPowerFlow)(method_result) if method_result else None

    def results_for_point_load_load_case(self, design_entity_analysis: '_6189.PointLoadLoadCase') -> '_3319.PointLoadPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PointLoadLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.PointLoadPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3319.PointLoadPowerFlow)(method_result) if method_result else None

    def results_for_power_load(self, design_entity: '_2034.PowerLoad') -> '_3322.PowerLoadPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PowerLoad)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.PowerLoadPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3322.PowerLoadPowerFlow)(method_result) if method_result else None

    def results_for_power_load_load_case(self, design_entity_analysis: '_6190.PowerLoadLoadCase') -> '_3322.PowerLoadPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PowerLoadLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.PowerLoadPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3322.PowerLoadPowerFlow)(method_result) if method_result else None

    def results_for_root_assembly(self, design_entity: '_2036.RootAssembly') -> '_3327.RootAssemblyPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.RootAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.RootAssemblyPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3327.RootAssemblyPowerFlow)(method_result) if method_result else None

    def results_for_root_assembly_load_case(self, design_entity_analysis: '_6196.RootAssemblyLoadCase') -> '_3327.RootAssemblyPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RootAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.RootAssemblyPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3327.RootAssemblyPowerFlow)(method_result) if method_result else None

    def results_for_specialised_assembly(self, design_entity: '_2038.SpecialisedAssembly') -> '_3331.SpecialisedAssemblyPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.SpecialisedAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.SpecialisedAssemblyPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3331.SpecialisedAssemblyPowerFlow)(method_result) if method_result else None

    def results_for_specialised_assembly_load_case(self, design_entity_analysis: '_6200.SpecialisedAssemblyLoadCase') -> '_3331.SpecialisedAssemblyPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpecialisedAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.SpecialisedAssemblyPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3331.SpecialisedAssemblyPowerFlow)(method_result) if method_result else None

    def results_for_unbalanced_mass(self, design_entity: '_2039.UnbalancedMass') -> '_3355.UnbalancedMassPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.UnbalancedMass)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.UnbalancedMassPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3355.UnbalancedMassPowerFlow)(method_result) if method_result else None

    def results_for_unbalanced_mass_load_case(self, design_entity_analysis: '_6231.UnbalancedMassLoadCase') -> '_3355.UnbalancedMassPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.UnbalancedMassLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.UnbalancedMassPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3355.UnbalancedMassPowerFlow)(method_result) if method_result else None

    def results_for_virtual_component(self, design_entity: '_2040.VirtualComponent') -> '_3356.VirtualComponentPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.VirtualComponent)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.VirtualComponentPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3356.VirtualComponentPowerFlow)(method_result) if method_result else None

    def results_for_virtual_component_load_case(self, design_entity_analysis: '_6232.VirtualComponentLoadCase') -> '_3356.VirtualComponentPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.VirtualComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.VirtualComponentPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3356.VirtualComponentPowerFlow)(method_result) if method_result else None

    def results_for_shaft(self, design_entity: '_2043.Shaft') -> '_3329.ShaftPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.shaft_model.Shaft)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ShaftPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3329.ShaftPowerFlow)(method_result) if method_result else None

    def results_for_shaft_load_case(self, design_entity_analysis: '_6198.ShaftLoadCase') -> '_3329.ShaftPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ShaftLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ShaftPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3329.ShaftPowerFlow)(method_result) if method_result else None

    def results_for_concept_gear(self, design_entity: '_2081.ConceptGear') -> '_3266.ConceptGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGear)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ConceptGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3266.ConceptGearPowerFlow)(method_result) if method_result else None

    def results_for_concept_gear_load_case(self, design_entity_analysis: '_6099.ConceptGearLoadCase') -> '_3266.ConceptGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ConceptGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3266.ConceptGearPowerFlow)(method_result) if method_result else None

    def results_for_concept_gear_set(self, design_entity: '_2082.ConceptGearSet') -> '_3267.ConceptGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ConceptGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3267.ConceptGearSetPowerFlow)(method_result) if method_result else None

    def results_for_concept_gear_set_load_case(self, design_entity_analysis: '_6101.ConceptGearSetLoadCase') -> '_3267.ConceptGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ConceptGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3267.ConceptGearSetPowerFlow)(method_result) if method_result else None

    def results_for_face_gear(self, design_entity: '_2088.FaceGear') -> '_3287.FaceGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGear)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.FaceGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3287.FaceGearPowerFlow)(method_result) if method_result else None

    def results_for_face_gear_load_case(self, design_entity_analysis: '_6137.FaceGearLoadCase') -> '_3287.FaceGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FaceGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.FaceGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3287.FaceGearPowerFlow)(method_result) if method_result else None

    def results_for_face_gear_set(self, design_entity: '_2089.FaceGearSet') -> '_3288.FaceGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.FaceGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3288.FaceGearSetPowerFlow)(method_result) if method_result else None

    def results_for_face_gear_set_load_case(self, design_entity_analysis: '_6139.FaceGearSetLoadCase') -> '_3288.FaceGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FaceGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.FaceGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3288.FaceGearSetPowerFlow)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear(self, design_entity: '_2073.AGMAGleasonConicalGear') -> '_3241.AGMAGleasonConicalGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGear)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.AGMAGleasonConicalGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3241.AGMAGleasonConicalGearPowerFlow)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_load_case(self, design_entity_analysis: '_6073.AGMAGleasonConicalGearLoadCase') -> '_3241.AGMAGleasonConicalGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.AGMAGleasonConicalGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3241.AGMAGleasonConicalGearPowerFlow)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_set(self, design_entity: '_2074.AGMAGleasonConicalGearSet') -> '_3242.AGMAGleasonConicalGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.AGMAGleasonConicalGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3242.AGMAGleasonConicalGearSetPowerFlow)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_set_load_case(self, design_entity_analysis: '_6075.AGMAGleasonConicalGearSetLoadCase') -> '_3242.AGMAGleasonConicalGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.AGMAGleasonConicalGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3242.AGMAGleasonConicalGearSetPowerFlow)(method_result) if method_result else None

    def results_for_bevel_differential_gear(self, design_entity: '_2075.BevelDifferentialGear') -> '_3248.BevelDifferentialGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGear)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BevelDifferentialGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3248.BevelDifferentialGearPowerFlow)(method_result) if method_result else None

    def results_for_bevel_differential_gear_load_case(self, design_entity_analysis: '_6081.BevelDifferentialGearLoadCase') -> '_3248.BevelDifferentialGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BevelDifferentialGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3248.BevelDifferentialGearPowerFlow)(method_result) if method_result else None

    def results_for_bevel_differential_gear_set(self, design_entity: '_2076.BevelDifferentialGearSet') -> '_3249.BevelDifferentialGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BevelDifferentialGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3249.BevelDifferentialGearSetPowerFlow)(method_result) if method_result else None

    def results_for_bevel_differential_gear_set_load_case(self, design_entity_analysis: '_6083.BevelDifferentialGearSetLoadCase') -> '_3249.BevelDifferentialGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BevelDifferentialGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3249.BevelDifferentialGearSetPowerFlow)(method_result) if method_result else None

    def results_for_bevel_differential_planet_gear(self, design_entity: '_2077.BevelDifferentialPlanetGear') -> '_3250.BevelDifferentialPlanetGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialPlanetGear)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BevelDifferentialPlanetGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3250.BevelDifferentialPlanetGearPowerFlow)(method_result) if method_result else None

    def results_for_bevel_differential_planet_gear_load_case(self, design_entity_analysis: '_6084.BevelDifferentialPlanetGearLoadCase') -> '_3250.BevelDifferentialPlanetGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialPlanetGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BevelDifferentialPlanetGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3250.BevelDifferentialPlanetGearPowerFlow)(method_result) if method_result else None

    def results_for_bevel_differential_sun_gear(self, design_entity: '_2078.BevelDifferentialSunGear') -> '_3251.BevelDifferentialSunGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialSunGear)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BevelDifferentialSunGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3251.BevelDifferentialSunGearPowerFlow)(method_result) if method_result else None

    def results_for_bevel_differential_sun_gear_load_case(self, design_entity_analysis: '_6085.BevelDifferentialSunGearLoadCase') -> '_3251.BevelDifferentialSunGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialSunGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BevelDifferentialSunGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3251.BevelDifferentialSunGearPowerFlow)(method_result) if method_result else None

    def results_for_bevel_gear(self, design_entity: '_2079.BevelGear') -> '_3253.BevelGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BevelGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3253.BevelGearPowerFlow)(method_result) if method_result else None

    def results_for_bevel_gear_load_case(self, design_entity_analysis: '_6086.BevelGearLoadCase') -> '_3253.BevelGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BevelGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3253.BevelGearPowerFlow)(method_result) if method_result else None

    def results_for_bevel_gear_set(self, design_entity: '_2080.BevelGearSet') -> '_3254.BevelGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BevelGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3254.BevelGearSetPowerFlow)(method_result) if method_result else None

    def results_for_bevel_gear_set_load_case(self, design_entity_analysis: '_6088.BevelGearSetLoadCase') -> '_3254.BevelGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BevelGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3254.BevelGearSetPowerFlow)(method_result) if method_result else None

    def results_for_conical_gear(self, design_entity: '_2083.ConicalGear') -> '_3269.ConicalGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGear)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ConicalGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3269.ConicalGearPowerFlow)(method_result) if method_result else None

    def results_for_conical_gear_load_case(self, design_entity_analysis: '_6102.ConicalGearLoadCase') -> '_3269.ConicalGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConicalGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ConicalGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3269.ConicalGearPowerFlow)(method_result) if method_result else None

    def results_for_conical_gear_set(self, design_entity: '_2084.ConicalGearSet') -> '_3270.ConicalGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ConicalGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3270.ConicalGearSetPowerFlow)(method_result) if method_result else None

    def results_for_conical_gear_set_load_case(self, design_entity_analysis: '_6106.ConicalGearSetLoadCase') -> '_3270.ConicalGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConicalGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ConicalGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3270.ConicalGearSetPowerFlow)(method_result) if method_result else None

    def results_for_cylindrical_gear(self, design_entity: '_2085.CylindricalGear') -> '_3281.CylindricalGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGear)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.CylindricalGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3281.CylindricalGearPowerFlow)(method_result) if method_result else None

    def results_for_cylindrical_gear_load_case(self, design_entity_analysis: '_6115.CylindricalGearLoadCase') -> '_3281.CylindricalGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CylindricalGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.CylindricalGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3281.CylindricalGearPowerFlow)(method_result) if method_result else None

    def results_for_cylindrical_gear_set(self, design_entity: '_2086.CylindricalGearSet') -> '_3282.CylindricalGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.CylindricalGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3282.CylindricalGearSetPowerFlow)(method_result) if method_result else None

    def results_for_cylindrical_gear_set_load_case(self, design_entity_analysis: '_6119.CylindricalGearSetLoadCase') -> '_3282.CylindricalGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CylindricalGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.CylindricalGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3282.CylindricalGearSetPowerFlow)(method_result) if method_result else None

    def results_for_cylindrical_planet_gear(self, design_entity: '_2087.CylindricalPlanetGear') -> '_3283.CylindricalPlanetGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalPlanetGear)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.CylindricalPlanetGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3283.CylindricalPlanetGearPowerFlow)(method_result) if method_result else None

    def results_for_cylindrical_planet_gear_load_case(self, design_entity_analysis: '_6120.CylindricalPlanetGearLoadCase') -> '_3283.CylindricalPlanetGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CylindricalPlanetGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.CylindricalPlanetGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3283.CylindricalPlanetGearPowerFlow)(method_result) if method_result else None

    def results_for_gear(self, design_entity: '_2090.Gear') -> '_3291.GearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.Gear)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.GearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3291.GearPowerFlow)(method_result) if method_result else None

    def results_for_gear_load_case(self, design_entity_analysis: '_6142.GearLoadCase') -> '_3291.GearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.GearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.GearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3291.GearPowerFlow)(method_result) if method_result else None

    def results_for_gear_set(self, design_entity: '_2092.GearSet') -> '_3292.GearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.GearSet)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.GearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3292.GearSetPowerFlow)(method_result) if method_result else None

    def results_for_gear_set_load_case(self, design_entity_analysis: '_6147.GearSetLoadCase') -> '_3292.GearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.GearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.GearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3292.GearSetPowerFlow)(method_result) if method_result else None

    def results_for_hypoid_gear(self, design_entity: '_2094.HypoidGear') -> '_3295.HypoidGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGear)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.HypoidGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3295.HypoidGearPowerFlow)(method_result) if method_result else None

    def results_for_hypoid_gear_load_case(self, design_entity_analysis: '_6157.HypoidGearLoadCase') -> '_3295.HypoidGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.HypoidGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.HypoidGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3295.HypoidGearPowerFlow)(method_result) if method_result else None

    def results_for_hypoid_gear_set(self, design_entity: '_2095.HypoidGearSet') -> '_3296.HypoidGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.HypoidGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3296.HypoidGearSetPowerFlow)(method_result) if method_result else None

    def results_for_hypoid_gear_set_load_case(self, design_entity_analysis: '_6159.HypoidGearSetLoadCase') -> '_3296.HypoidGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.HypoidGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.HypoidGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3296.HypoidGearSetPowerFlow)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear(self, design_entity: '_2096.KlingelnbergCycloPalloidConicalGear') -> '_3300.KlingelnbergCycloPalloidConicalGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGear)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.KlingelnbergCycloPalloidConicalGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3300.KlingelnbergCycloPalloidConicalGearPowerFlow)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_load_case(self, design_entity_analysis: '_6163.KlingelnbergCycloPalloidConicalGearLoadCase') -> '_3300.KlingelnbergCycloPalloidConicalGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.KlingelnbergCycloPalloidConicalGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3300.KlingelnbergCycloPalloidConicalGearPowerFlow)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_set(self, design_entity: '_2097.KlingelnbergCycloPalloidConicalGearSet') -> '_3301.KlingelnbergCycloPalloidConicalGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.KlingelnbergCycloPalloidConicalGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3301.KlingelnbergCycloPalloidConicalGearSetPowerFlow)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_set_load_case(self, design_entity_analysis: '_6165.KlingelnbergCycloPalloidConicalGearSetLoadCase') -> '_3301.KlingelnbergCycloPalloidConicalGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.KlingelnbergCycloPalloidConicalGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3301.KlingelnbergCycloPalloidConicalGearSetPowerFlow)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear(self, design_entity: '_2098.KlingelnbergCycloPalloidHypoidGear') -> '_3303.KlingelnbergCycloPalloidHypoidGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGear)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.KlingelnbergCycloPalloidHypoidGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3303.KlingelnbergCycloPalloidHypoidGearPowerFlow)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_load_case(self, design_entity_analysis: '_6166.KlingelnbergCycloPalloidHypoidGearLoadCase') -> '_3303.KlingelnbergCycloPalloidHypoidGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.KlingelnbergCycloPalloidHypoidGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3303.KlingelnbergCycloPalloidHypoidGearPowerFlow)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_set(self, design_entity: '_2099.KlingelnbergCycloPalloidHypoidGearSet') -> '_3304.KlingelnbergCycloPalloidHypoidGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.KlingelnbergCycloPalloidHypoidGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3304.KlingelnbergCycloPalloidHypoidGearSetPowerFlow)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_set_load_case(self, design_entity_analysis: '_6168.KlingelnbergCycloPalloidHypoidGearSetLoadCase') -> '_3304.KlingelnbergCycloPalloidHypoidGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.KlingelnbergCycloPalloidHypoidGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3304.KlingelnbergCycloPalloidHypoidGearSetPowerFlow)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear(self, design_entity: '_2100.KlingelnbergCycloPalloidSpiralBevelGear') -> '_3306.KlingelnbergCycloPalloidSpiralBevelGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.KlingelnbergCycloPalloidSpiralBevelGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3306.KlingelnbergCycloPalloidSpiralBevelGearPowerFlow)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_load_case(self, design_entity_analysis: '_6169.KlingelnbergCycloPalloidSpiralBevelGearLoadCase') -> '_3306.KlingelnbergCycloPalloidSpiralBevelGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.KlingelnbergCycloPalloidSpiralBevelGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3306.KlingelnbergCycloPalloidSpiralBevelGearPowerFlow)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self, design_entity: '_2101.KlingelnbergCycloPalloidSpiralBevelGearSet') -> '_3307.KlingelnbergCycloPalloidSpiralBevelGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.KlingelnbergCycloPalloidSpiralBevelGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3307.KlingelnbergCycloPalloidSpiralBevelGearSetPowerFlow)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_set_load_case(self, design_entity_analysis: '_6171.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase') -> '_3307.KlingelnbergCycloPalloidSpiralBevelGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.KlingelnbergCycloPalloidSpiralBevelGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3307.KlingelnbergCycloPalloidSpiralBevelGearSetPowerFlow)(method_result) if method_result else None

    def results_for_planetary_gear_set(self, design_entity: '_2102.PlanetaryGearSet') -> '_3317.PlanetaryGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.PlanetaryGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.PlanetaryGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3317.PlanetaryGearSetPowerFlow)(method_result) if method_result else None

    def results_for_planetary_gear_set_load_case(self, design_entity_analysis: '_6184.PlanetaryGearSetLoadCase') -> '_3317.PlanetaryGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PlanetaryGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.PlanetaryGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3317.PlanetaryGearSetPowerFlow)(method_result) if method_result else None

    def results_for_spiral_bevel_gear(self, design_entity: '_2103.SpiralBevelGear') -> '_3333.SpiralBevelGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.SpiralBevelGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3333.SpiralBevelGearPowerFlow)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_load_case(self, design_entity_analysis: '_6202.SpiralBevelGearLoadCase') -> '_3333.SpiralBevelGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.SpiralBevelGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3333.SpiralBevelGearPowerFlow)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_set(self, design_entity: '_2104.SpiralBevelGearSet') -> '_3334.SpiralBevelGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.SpiralBevelGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3334.SpiralBevelGearSetPowerFlow)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_set_load_case(self, design_entity_analysis: '_6204.SpiralBevelGearSetLoadCase') -> '_3334.SpiralBevelGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.SpiralBevelGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3334.SpiralBevelGearSetPowerFlow)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear(self, design_entity: '_2105.StraightBevelDiffGear') -> '_3339.StraightBevelDiffGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGear)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.StraightBevelDiffGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3339.StraightBevelDiffGearPowerFlow)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_load_case(self, design_entity_analysis: '_6209.StraightBevelDiffGearLoadCase') -> '_3339.StraightBevelDiffGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.StraightBevelDiffGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3339.StraightBevelDiffGearPowerFlow)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_set(self, design_entity: '_2106.StraightBevelDiffGearSet') -> '_3340.StraightBevelDiffGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.StraightBevelDiffGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3340.StraightBevelDiffGearSetPowerFlow)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_set_load_case(self, design_entity_analysis: '_6211.StraightBevelDiffGearSetLoadCase') -> '_3340.StraightBevelDiffGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.StraightBevelDiffGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3340.StraightBevelDiffGearSetPowerFlow)(method_result) if method_result else None

    def results_for_straight_bevel_gear(self, design_entity: '_2107.StraightBevelGear') -> '_3342.StraightBevelGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.StraightBevelGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3342.StraightBevelGearPowerFlow)(method_result) if method_result else None

    def results_for_straight_bevel_gear_load_case(self, design_entity_analysis: '_6212.StraightBevelGearLoadCase') -> '_3342.StraightBevelGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.StraightBevelGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3342.StraightBevelGearPowerFlow)(method_result) if method_result else None

    def results_for_straight_bevel_gear_set(self, design_entity: '_2108.StraightBevelGearSet') -> '_3343.StraightBevelGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.StraightBevelGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3343.StraightBevelGearSetPowerFlow)(method_result) if method_result else None

    def results_for_straight_bevel_gear_set_load_case(self, design_entity_analysis: '_6214.StraightBevelGearSetLoadCase') -> '_3343.StraightBevelGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.StraightBevelGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3343.StraightBevelGearSetPowerFlow)(method_result) if method_result else None

    def results_for_straight_bevel_planet_gear(self, design_entity: '_2109.StraightBevelPlanetGear') -> '_3344.StraightBevelPlanetGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelPlanetGear)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.StraightBevelPlanetGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3344.StraightBevelPlanetGearPowerFlow)(method_result) if method_result else None

    def results_for_straight_bevel_planet_gear_load_case(self, design_entity_analysis: '_6215.StraightBevelPlanetGearLoadCase') -> '_3344.StraightBevelPlanetGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelPlanetGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.StraightBevelPlanetGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3344.StraightBevelPlanetGearPowerFlow)(method_result) if method_result else None

    def results_for_straight_bevel_sun_gear(self, design_entity: '_2110.StraightBevelSunGear') -> '_3345.StraightBevelSunGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelSunGear)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.StraightBevelSunGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3345.StraightBevelSunGearPowerFlow)(method_result) if method_result else None

    def results_for_straight_bevel_sun_gear_load_case(self, design_entity_analysis: '_6216.StraightBevelSunGearLoadCase') -> '_3345.StraightBevelSunGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelSunGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.StraightBevelSunGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3345.StraightBevelSunGearPowerFlow)(method_result) if method_result else None

    def results_for_worm_gear(self, design_entity: '_2111.WormGear') -> '_3358.WormGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGear)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.WormGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3358.WormGearPowerFlow)(method_result) if method_result else None

    def results_for_worm_gear_load_case(self, design_entity_analysis: '_6233.WormGearLoadCase') -> '_3358.WormGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.WormGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.WormGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3358.WormGearPowerFlow)(method_result) if method_result else None

    def results_for_worm_gear_set(self, design_entity: '_2112.WormGearSet') -> '_3359.WormGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.WormGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3359.WormGearSetPowerFlow)(method_result) if method_result else None
