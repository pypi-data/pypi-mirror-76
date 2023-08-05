﻿'''_5070.py

MultiBodyDynamicsAnalysis
'''


from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.mbd_analyses import _5066
from mastapy.nodal_analysis.system_solvers import (
    _1427, _1409, _1410, _1413,
    _1414, _1415, _1416, _1417,
    _1418, _1419, _1420, _1425,
    _1428
)
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.analysis_cases import _6522
from mastapy._internal.python_net import python_net_import

_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'MultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('MultiBodyDynamicsAnalysis',)


class MultiBodyDynamicsAnalysis(_6522.TimeSeriesLoadAnalysisCase):
    '''MultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def percentage_time_spent_in_masta_solver(self) -> 'float':
        '''float: 'PercentageTimeSpentInMASTASolver' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.PercentageTimeSpentInMASTASolver

    @property
    def has_interface_analysis_results_available(self) -> 'bool':
        '''bool: 'HasInterfaceAnalysisResultsAvailable' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.HasInterfaceAnalysisResultsAvailable

    @property
    def mbd_options(self) -> '_5066.MBDAnalysisOptions':
        '''MBDAnalysisOptions: 'MBDOptions' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5066.MBDAnalysisOptions)(self.wrapped.MBDOptions) if self.wrapped.MBDOptions else None

    @property
    def transient_solver(self) -> '_1427.TransientSolver':
        '''TransientSolver: 'TransientSolver' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1427.TransientSolver)(self.wrapped.TransientSolver) if self.wrapped.TransientSolver else None

    @property
    def transient_solver_of_type_backward_euler_acceleration_step_halving_transient_solver(self) -> '_1409.BackwardEulerAccelerationStepHalvingTransientSolver':
        '''BackwardEulerAccelerationStepHalvingTransientSolver: 'TransientSolver' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1409.BackwardEulerAccelerationStepHalvingTransientSolver.TYPE not in self.wrapped.TransientSolver.__class__.__mro__:
            raise CastException('Failed to cast transient_solver to BackwardEulerAccelerationStepHalvingTransientSolver. Expected: {}.'.format(self.wrapped.TransientSolver.__class__.__qualname__))

        return constructor.new(_1409.BackwardEulerAccelerationStepHalvingTransientSolver)(self.wrapped.TransientSolver) if self.wrapped.TransientSolver else None

    @property
    def transient_solver_of_type_backward_euler_transient_solver(self) -> '_1410.BackwardEulerTransientSolver':
        '''BackwardEulerTransientSolver: 'TransientSolver' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1410.BackwardEulerTransientSolver.TYPE not in self.wrapped.TransientSolver.__class__.__mro__:
            raise CastException('Failed to cast transient_solver to BackwardEulerTransientSolver. Expected: {}.'.format(self.wrapped.TransientSolver.__class__.__qualname__))

        return constructor.new(_1410.BackwardEulerTransientSolver)(self.wrapped.TransientSolver) if self.wrapped.TransientSolver else None

    @property
    def transient_solver_of_type_internal_transient_solver(self) -> '_1413.InternalTransientSolver':
        '''InternalTransientSolver: 'TransientSolver' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1413.InternalTransientSolver.TYPE not in self.wrapped.TransientSolver.__class__.__mro__:
            raise CastException('Failed to cast transient_solver to InternalTransientSolver. Expected: {}.'.format(self.wrapped.TransientSolver.__class__.__qualname__))

        return constructor.new(_1413.InternalTransientSolver)(self.wrapped.TransientSolver) if self.wrapped.TransientSolver else None

    @property
    def transient_solver_of_type_lobatto_iiia_transient_solver(self) -> '_1414.LobattoIIIATransientSolver':
        '''LobattoIIIATransientSolver: 'TransientSolver' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1414.LobattoIIIATransientSolver.TYPE not in self.wrapped.TransientSolver.__class__.__mro__:
            raise CastException('Failed to cast transient_solver to LobattoIIIATransientSolver. Expected: {}.'.format(self.wrapped.TransientSolver.__class__.__qualname__))

        return constructor.new(_1414.LobattoIIIATransientSolver)(self.wrapped.TransientSolver) if self.wrapped.TransientSolver else None

    @property
    def transient_solver_of_type_lobatto_iiic_transient_solver(self) -> '_1415.LobattoIIICTransientSolver':
        '''LobattoIIICTransientSolver: 'TransientSolver' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1415.LobattoIIICTransientSolver.TYPE not in self.wrapped.TransientSolver.__class__.__mro__:
            raise CastException('Failed to cast transient_solver to LobattoIIICTransientSolver. Expected: {}.'.format(self.wrapped.TransientSolver.__class__.__qualname__))

        return constructor.new(_1415.LobattoIIICTransientSolver)(self.wrapped.TransientSolver) if self.wrapped.TransientSolver else None

    @property
    def transient_solver_of_type_newmark_acceleration_transient_solver(self) -> '_1416.NewmarkAccelerationTransientSolver':
        '''NewmarkAccelerationTransientSolver: 'TransientSolver' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1416.NewmarkAccelerationTransientSolver.TYPE not in self.wrapped.TransientSolver.__class__.__mro__:
            raise CastException('Failed to cast transient_solver to NewmarkAccelerationTransientSolver. Expected: {}.'.format(self.wrapped.TransientSolver.__class__.__qualname__))

        return constructor.new(_1416.NewmarkAccelerationTransientSolver)(self.wrapped.TransientSolver) if self.wrapped.TransientSolver else None

    @property
    def transient_solver_of_type_newmark_transient_solver(self) -> '_1417.NewmarkTransientSolver':
        '''NewmarkTransientSolver: 'TransientSolver' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1417.NewmarkTransientSolver.TYPE not in self.wrapped.TransientSolver.__class__.__mro__:
            raise CastException('Failed to cast transient_solver to NewmarkTransientSolver. Expected: {}.'.format(self.wrapped.TransientSolver.__class__.__qualname__))

        return constructor.new(_1417.NewmarkTransientSolver)(self.wrapped.TransientSolver) if self.wrapped.TransientSolver else None

    @property
    def transient_solver_of_type_semi_implicit_transient_solver(self) -> '_1418.SemiImplicitTransientSolver':
        '''SemiImplicitTransientSolver: 'TransientSolver' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1418.SemiImplicitTransientSolver.TYPE not in self.wrapped.TransientSolver.__class__.__mro__:
            raise CastException('Failed to cast transient_solver to SemiImplicitTransientSolver. Expected: {}.'.format(self.wrapped.TransientSolver.__class__.__qualname__))

        return constructor.new(_1418.SemiImplicitTransientSolver)(self.wrapped.TransientSolver) if self.wrapped.TransientSolver else None

    @property
    def transient_solver_of_type_simple_acceleration_based_step_halving_transient_solver(self) -> '_1419.SimpleAccelerationBasedStepHalvingTransientSolver':
        '''SimpleAccelerationBasedStepHalvingTransientSolver: 'TransientSolver' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1419.SimpleAccelerationBasedStepHalvingTransientSolver.TYPE not in self.wrapped.TransientSolver.__class__.__mro__:
            raise CastException('Failed to cast transient_solver to SimpleAccelerationBasedStepHalvingTransientSolver. Expected: {}.'.format(self.wrapped.TransientSolver.__class__.__qualname__))

        return constructor.new(_1419.SimpleAccelerationBasedStepHalvingTransientSolver)(self.wrapped.TransientSolver) if self.wrapped.TransientSolver else None

    @property
    def transient_solver_of_type_simple_velocity_based_step_halving_transient_solver(self) -> '_1420.SimpleVelocityBasedStepHalvingTransientSolver':
        '''SimpleVelocityBasedStepHalvingTransientSolver: 'TransientSolver' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1420.SimpleVelocityBasedStepHalvingTransientSolver.TYPE not in self.wrapped.TransientSolver.__class__.__mro__:
            raise CastException('Failed to cast transient_solver to SimpleVelocityBasedStepHalvingTransientSolver. Expected: {}.'.format(self.wrapped.TransientSolver.__class__.__qualname__))

        return constructor.new(_1420.SimpleVelocityBasedStepHalvingTransientSolver)(self.wrapped.TransientSolver) if self.wrapped.TransientSolver else None

    @property
    def transient_solver_of_type_step_halving_transient_solver(self) -> '_1425.StepHalvingTransientSolver':
        '''StepHalvingTransientSolver: 'TransientSolver' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1425.StepHalvingTransientSolver.TYPE not in self.wrapped.TransientSolver.__class__.__mro__:
            raise CastException('Failed to cast transient_solver to StepHalvingTransientSolver. Expected: {}.'.format(self.wrapped.TransientSolver.__class__.__qualname__))

        return constructor.new(_1425.StepHalvingTransientSolver)(self.wrapped.TransientSolver) if self.wrapped.TransientSolver else None

    @property
    def transient_solver_of_type_wilson_theta_transient_solver(self) -> '_1428.WilsonThetaTransientSolver':
        '''WilsonThetaTransientSolver: 'TransientSolver' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1428.WilsonThetaTransientSolver.TYPE not in self.wrapped.TransientSolver.__class__.__mro__:
            raise CastException('Failed to cast transient_solver to WilsonThetaTransientSolver. Expected: {}.'.format(self.wrapped.TransientSolver.__class__.__qualname__))

        return constructor.new(_1428.WilsonThetaTransientSolver)(self.wrapped.TransientSolver) if self.wrapped.TransientSolver else None
