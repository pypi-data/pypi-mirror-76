'''_5076.py

PlanetaryConnectionMultiBodyDynamicsAnalysis
'''


from mastapy.system_model.connections_and_sockets import _1867
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6183
from mastapy.system_model.analyses_and_results.mbd_analyses import _5090
from mastapy._internal.python_net import python_net_import

_PLANETARY_CONNECTION_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'PlanetaryConnectionMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetaryConnectionMultiBodyDynamicsAnalysis',)


class PlanetaryConnectionMultiBodyDynamicsAnalysis(_5090.ShaftToMountableComponentConnectionMultiBodyDynamicsAnalysis):
    '''PlanetaryConnectionMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _PLANETARY_CONNECTION_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlanetaryConnectionMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_1867.PlanetaryConnection':
        '''PlanetaryConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1867.PlanetaryConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6183.PlanetaryConnectionLoadCase':
        '''PlanetaryConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6183.PlanetaryConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None
