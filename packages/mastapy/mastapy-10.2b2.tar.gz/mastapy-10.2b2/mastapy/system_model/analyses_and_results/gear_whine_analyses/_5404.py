'''_5404.py

SynchroniserGearWhineAnalysis
'''


from mastapy.system_model.part_model.couplings import _2156
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6218
from mastapy.system_model.analyses_and_results.system_deflections import _2350
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5388
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'SynchroniserGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserGearWhineAnalysis',)


class SynchroniserGearWhineAnalysis(_5388.SpecialisedAssemblyGearWhineAnalysis):
    '''SynchroniserGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _SYNCHRONISER_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SynchroniserGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2156.Synchroniser':
        '''Synchroniser: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2156.Synchroniser)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6218.SynchroniserLoadCase':
        '''SynchroniserLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6218.SynchroniserLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def system_deflection_results(self) -> '_2350.SynchroniserSystemDeflection':
        '''SynchroniserSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2350.SynchroniserSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
