# -*- mode:python; coding: utf-8 -*-
# @file
# @section LICENSE
#
# Copyright (©) 2016-2020 EPFL (École Polytechnique Fédérale de Lausanne),
# Laboratory (LSMS - Laboratoire de Simulation en Mécanique des Solides)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
Pulling solvers to nonlinear_solvers module
"""
from functools import wraps

import numpy as np
from scipy.sparse.linalg import LinearOperator, lgmres
from scipy.linalg import norm
from scipy.optimize import newton_krylov, root
from scipy.optimize.nonlin import NoConvergence

from .. import EPSolver, Logger, LogLevel
from .._tamaas import _tolerance_manager
from .._tamaas import _DFSANESolver as DFSANECXXSolver


__all__ = ['NLNoConvergence',
           'DFSANESolver',
           'DFSANECXXSolver',
           'NewtonKrylovSolver',
           'ToleranceManager']


class NLNoConvergence(Exception):
    """Convergence not reached exception"""


class NewtonRaphsonSolver(EPSolver):
    """
    Newton-Raphson based on CTO
    """

    def __init__(self, residual, *args):
        NewtonRaphsonSolver.__init__(self, residual)
        self._residual = self.getResidual()
        self._x = self.getStrainIncrement()
        self.last_solution = np.zeros_like(self._x)

    def applyTangent(self, _input, strain):
        _input = np.reshape(_input, strain.shape)
        out = np.zeros_like(_input)
        self._residual.applyTangent(out, _input, strain)
        return out

    def solve(self):
        self._x[...] = 0

        # For initial guess, compute the strain due to boundary tractions
        self._residual.computeResidual(self._x)
        self._x[...] = self._residual.getVector()

        res_vec = np.ravel(self._residual.getVector())
        initial_norm = norm(res_vec)
        self._residual.computeResidual(self._x)

        n_max = 100
        i = 0

        while norm(res_vec) / initial_norm > 1e-10 and i < n_max:
            # Making linear tangent
            tangent = LinearOperator(
                (self._x.size, self._x.size),
                matvec=lambda x: self.applyTangent(x, self._x))
            res_vec *= -1
            correction, ok = lgmres(tangent, res_vec, tol=1e-12, maxiter=100)
            if ok != 0:
                raise Exception("LGMRES not converged")
            self._x += np.reshape(correction, self._x.shape)
            self._residual.computeResidual(self._x)
            i += 1

        Logger().get(LogLevel.info) << \
            "Solved Newton-Raphson in {} iterations".format(i)

        # Computing the strain correction
        self.last_solution *= -1
        self.last_solution += self._x

        # Computing displacements
        self._residual.computeResidualDisplacement(self.last_solution)
        self.last_solution[...] = self._x[...]


class ScipySolver(EPSolver):
    """
    Base class for solvers wrapping SciPy routines
    """

    def __init__(self, residual, _, callback=None):
        super(ScipySolver, self).__init__(residual)
        self.callback = callback
        self._x = self.getStrainIncrement()
        self._residual = self.getResidual()
        self.options = {'ftol': 0, 'fatol': 1e-9}

    def solve(self):
        """
        Solve the nonlinear plasticity equation using the scipy_solve routine
        """
        # For initial guess, compute the strain due to boundary tractions
        # self._residual.computeResidual(self._x)
        # self._x[...] = self._residual.getVector()
        EPSolver.beforeSolve(self)

        # Scipy root callback
        def compute_residual(vec):
            self._residual.computeResidual(vec)
            return self._residual.getVector().copy()

        # Solve
        self._x[...] = self.scipy_solve(compute_residual)

        # Computing displacements
        self._residual.computeResidualDisplacement(self._x)

    def reset(self):
        "Set solution vector to zero"
        self._x[...] = 0


class NewtonKrylovSolver(ScipySolver):
    """
    Solve using a finite-difference Newton-Krylov method
    """

    def __init__(self, residual, model=None, callback=None):
        ScipySolver.__init__(self, residual, model,
                             callback=callback)

    def scipy_solve(self, compute_residual):
        "Solve R(delta epsilon) = 0 using a newton-krylov method"
        try:
            return newton_krylov(compute_residual, self._x,
                                 f_tol=self.tolerance,
                                 verbose=True, callback=self.callback)
        except NoConvergence:
            raise NLNoConvergence("Newton-Krylov did not converge")


class DFSANESolver(ScipySolver):
    """
    Solve using a spectral residual jacobianless method
    """

    def __init__(self, residual, model=None, callback=None):
        ScipySolver.__init__(self, residual, model,
                             callback=callback)

    def scipy_solve(self, compute_residual):
        "Solve R(delta epsilon) = 0 using a df-sane method"
        solution = root(compute_residual,
                        self._x,
                        method='df-sane',
                        options={'ftol': 0, 'fatol': self.tolerance},
                        callback=self.callback)
        Logger().get(LogLevel.info) << \
            "DF-SANE/Scipy: {} ({} iterations, {})".format(
                solution.message,
                solution.nit,
                self.tolerance)

        if not solution.success:
            raise NLNoConvergence("DF-SANE/Scipy did not converge")
        return solution.x.copy()


def ToleranceManager(start, end, rate):
    "Decorator to manage tolerance of non-linear solver"
    # start /= rate  # just anticipating first multiplication

    def actual_decorator(cls):
        orig_init = cls.__init__
        orig_solve = cls.solve
        orig_update_state = cls.updateState

        @wraps(cls.__init__)
        def __init__(obj, *args, **kwargs):
            orig_init(obj, *args, **kwargs)
            obj.setToleranceManager(_tolerance_manager(start, end, rate))

        @wraps(cls.solve)
        def new_solve(obj, *args, **kwargs):
            ftol = obj.tolerance
            ftol *= rate

            obj.tolerance = max(ftol, end)
            return orig_solve(obj, *args, **kwargs)

        @wraps(cls.updateState)
        def updateState(obj, *args, **kwargs):
            obj.tolerance = start
            return orig_update_state(obj, *args, **kwargs)

        cls.__init__ = __init__
        # cls.solve = new_solve
        # cls.updateState = updateState
        return cls

    return actual_decorator
