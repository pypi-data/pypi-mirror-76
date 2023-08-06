"""Provide a simple way to build ODE models."""

import abc
import numpy as np
import pypfilt
import scipy.integrate


class Ode(pypfilt.Model):
    """A class that implements generic ODE models."""

    @abc.abstractmethod
    def init(self, ctx, vec):
        """
        Initialise state vectors.

        :param ctx: The simulation context.
        :param vec: An array of empty state vectors.
        """
        pass

    @abc.abstractmethod
    def state_size(self):
        pass

    @abc.abstractmethod
    def population_size(self):
        pass

    @abc.abstractmethod
    def describe(self):
        pass

    @abc.abstractmethod
    def pr_inf(self, prev, curr):
        pass

    @abc.abstractmethod
    def priors(self, params):
        pass

    @abc.abstractmethod
    def rates(self, xt, t, ctx, time, is_fs):
        """
        Calculate the derivatives of each compartment.

        :param xt: The 2D matrix of static vectors, which has shape ``(P, S)``
            for P particles and state vectors of length S.
        :param t: The current (scalar) time.
        :param ctx: The simulation context.
        :param time: The current time-step.
        :param is_fs: Indicates whether this is a forecasting simulation.
        """
        pass

    def d_dt(self, t, xt, ctx, time, is_fs):
        """Calculate the derivatives of each compartment."""
        # Restore the 2D shape of the flattened state matrix.
        xt = xt.reshape((-1, self.state_size()))
        dt = self.rates(xt, t, ctx, time, is_fs)
        # Flatten the 2D derivatives matrix.
        return dt.reshape(-1)

    def update(self, ctx, time, dt, is_fs, prev, curr):
        """Perform a single time-step.

        :param ctx: The simulation context.
        :param time: The current time-step.
        :param dt: The time-step size (days).
        :param is_fs: Indicates whether this is a forecasting simulation.
        :param prev: The state before the time-step.
        :param curr: The state after the time-step (destructively updated).
        """
        t = ctx.component['time'].to_scalar(time)
        print('t = {}'.format(t))
        print(np.amax(prev, axis=0))
        # The state matrix must be flattened for solve_ivp().
        soln = scipy.integrate.solve_ivp(
            self.d_dt,
            [t, t + dt],
            prev.reshape(-1),
            args=(ctx, time, is_fs))
        # Restore the 2D shape of the flattened state matrix.
        curr[:] = soln.y[..., -1].reshape(curr.shape)
        print(np.amax(curr, axis=0))

    def num_inf(self, prev, curr):
        return self.population_size() * self.pr_inf(prev, curr)

    @abc.abstractmethod
    def is_seeded(self, hist):
        """Identify state vectors where infections have occurred.

        :param hist: A matrix of arbitrary dimensions, whose final dimension
            covers the model state space (i.e., has a length no smaller than
            that returned by :py:func:`state_size`).
        :type hist: numpy.ndarray

        :returns: A matrix of one fewer dimensions than ``hist`` that contains
            ``1`` for state vectors where infections have occurred and ``0``
            for state vectors where they have not.
        :rtype: numpy.ndarray
        """
        pass


class SEEIIR(Ode):

    __info = [
        ("S", False, 0, 1), ("E1", False, 0, 1), ("E2", False, 0, 1),
        ("I1", False, 0, 1), ("I2", False, 0, 1), ("R", False, 0, 1),
        ("R0", True, 1, 2), ("sigma", True, 1/3, 2),
        ("gamma", True, 1/3, 1), ("t0", False, 0, 100)]

    ix_S = 0
    ix_E1 = 1
    ix_E2 = 2
    ix_I1 = 3
    ix_I2 = 4
    ix_R = 5
    ix_R0 = 6
    ix_sigma = 7
    ix_gamma = 8
    ix_t0 = 9

    """A class that implements generic ODE models."""
    def init(self, ctx, vec):
        """
        Initialise state vectors.

        :param ctx: The simulation context.
        :param vec: An array of empty state vectors.
        """
        self.popn_size = ctx.params['model']['population_size']
        prior = ctx.params['model']['prior']
        rnd_size = vec[..., 0].shape
        rnd = ctx.component['random']['model']

        num_exps = 10.0
        vec[..., :] = 0
        vec[..., 0] = 1.0 - num_exps / self.popn_size
        vec[..., 1] = num_exps / self.popn_size
        vec[..., self.ix_R0] = prior['R0'](rnd, size=rnd_size)
        vec[..., self.ix_sigma] = prior['sigma'](rnd, size=rnd_size)
        vec[..., self.ix_gamma] = prior['gamma'](rnd, size=rnd_size)
        vec[..., self.ix_t0] = prior['t0'](rnd, size=rnd_size)

        # Allow R0 and imported cases to be provided via lookup tables.
        self.__R0_lookup = None
        self.__Forcing_lookup = None
        # NOTE: this isn't called when state is loaded from cache, so the
        # lookup tables will be undefined and raise an exception. This is
        # preferable to setting them both to `None` in the constructor, since
        # the cache logic cannot currently check whether the lookup tables
        # have changed, and so it's potentially invalid to restore the cached
        # state.
        if 'lookup' in ctx.component:
            tables = ctx.component['lookup']
            if 'R0' in tables:
                self.__R0_lookup = tables['R0']
                num_values = self.__R0_lookup.value_count()
                print('Using lookup table for R0 with {} values'.format(
                    num_values))
                if num_values > 1:
                    vec[..., self.ix_R0] = rnd.integers(num_values,
                                                        size=rnd_size)
                else:
                    vec[..., self.ix_R0] = 0
            if 'R0_forcing' in tables:
                self.__Forcing_lookup = tables['R0_forcing']
                print('Using lookup table for forcing with {} values'
                      .format(self.__Forcing_lookup.value_count()))

    def state_size(self):
        return len(self.__info)

    def population_size(self):
        return self.popn_size

    def describe(self):
        return self.__info

    def pr_inf(self, prev, curr):
        """
        Calculate the likelihood of an individual becoming infected, for any
        number of state vectors.

        :param prev: The model states at the start of the observation period.
        :param curr: The model states at the end of the observation period.
        """
        # Count the number of susceptible / exposed individuals at both ends
        # of the simulation period.
        prev_amt = np.sum(prev[..., :self.ix_I2], axis=-1)
        curr_amt = np.sum(curr[..., :self.ix_I2], axis=-1)
        # Avoid returning very small negative values (e.g., -1e-10).
        return np.maximum(prev_amt - curr_amt, 0)

    def priors(self, params):
        """
        Return a dictionary of model parameter priors.

        :param params: Simulation parameters.
        """
        # Sample R0, eta and alpha from uniform distributions.
        R0_l, l_l, i_l, t0_l = params['model']['param_min'][self.ix_R0:]
        R0_u, l_u, i_u, t0_u = params['model']['param_max'][self.ix_R0:]
        # Sample sigma and gamma from inverse uniform distributions.
        # l_l, l_u, i_l, i_u = 1 / l_l, 1 / l_u, 1 / i_l, 1 / i_u
        priors = {
            # The basic reproduction number.
            'R0': lambda r, size=None: r.uniform(R0_l, R0_u, size=size),
            # Inverse of the incubation period (days^-1).
            'sigma': lambda r, size=None: 1 / r.uniform(l_l, l_u, size=size),
            # Inverse of the infectious period (days^-1).
            'gamma': lambda r, size=None: 1 / r.uniform(i_l, i_u, size=size),
            # Time of first exposure event.
            't0': lambda r, size=None: r.uniform(t0_l, t0_u, size=size),
        }
        return priors

    def rates(self, xt, t, ctx, time, is_fs):
        """
        Calculate the derivatives of each compartment.

        :param xt: The 2D matrix of static vectors, which has shape ``(P, S)``
            for P particles and state vectors of length S.
        :param t: The current (scalar) time.
        :param ctx: The simulation context.
        :param time: The current (native scale) time.
        :param is_fs: Indicates whether this is a forecasting simulation.
        """
        # Prevent negative values.
        xt[xt < 0] = 0

        # Extract parameters.
        R0 = xt[..., self.ix_R0].copy()
        sigma = xt[..., self.ix_sigma].copy()
        gamma = xt[..., self.ix_gamma].copy()
        t0 = xt[..., self.ix_t0]

        # Look up R0 values, if appropriate.
        if self.__R0_lookup is not None:
            start = ctx.component['time'].start
            if start == ctx.params['epoch']:
                # NOTE: Estimation run, use Reff(t).
                when = time
            else:
                # NOTE: Forecasting run, use Reff(forecast_date).
                when = start
            # Retrieve R0 values from the lookup table.
            R0_values = self.__R0_lookup.lookup(when)
            R0_ixs = R0.astype(int)
            R0 = R0_values[R0_ixs]

        # Set parameters to zero prior to time of initial exposures.
        zero_mask = t < t0
        R0[zero_mask] = 0
        sigma[zero_mask] = 0
        gamma[zero_mask] = 0
        beta = R0 * gamma

        s_to_e1 = (beta * (xt[..., self.ix_I1] + xt[..., self.ix_I2]) *
                   xt[..., self.ix_S])
        e1_to_e2 = 2 * sigma * xt[..., self.ix_E1]
        e2_to_i1 = 2 * sigma * xt[..., self.ix_E2]
        i1_to_i2 = 2 * gamma * xt[..., self.ix_I1]
        i2_to_r = 2 * gamma * xt[..., self.ix_I2]

        d_dt = np.zeros(xt.shape)
        d_dt[..., self.ix_S] = 0.0 - s_to_e1
        d_dt[..., self.ix_E1] = s_to_e1 - e1_to_e2
        d_dt[..., self.ix_E2] = e1_to_e2 - e2_to_i1
        d_dt[..., self.ix_I1] = e2_to_i1 - i1_to_i2
        d_dt[..., self.ix_I2] = i1_to_i2 - i2_to_r
        d_dt[..., self.ix_R] = i2_to_r

        return d_dt

    def is_seeded(self, hist):
        return np.ceil(1 - hist[..., self.ix_S])
