"""Stochastic compartmental models."""

import logging
from pathlib import Path
import numpy as np
import pypfilt
from .model import Model


class SEEIIR(Model):
    """A stochastic SEEIIR compartment model."""

    __info = [
        ("S", False, 0, 1), ("E1", False, 0, 1), ("E2", False, 0, 1),
        ("I1", False, 0, 1), ("I2", False, 0, 1), ("R", False, 0, 1),
        ("R0", True, 1.0, 2.0),
        ("sigma", True, 1/3, 2.0),
        ("gamma", True, 1/3, 1.0),
        ("t0", False, 0, 100),
        ("R0_ix", False, 0, 1e6),
        ("R0_val", False, 0, 100)]

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
    ix_R0_ix = 10
    ix_R0_val = 11

    def __init__(self):
        self.__R0_lookup = None
        self.__external_lookup = None
        self.__regularise_R0_ix = False

    def state_size(self):
        """Return the size of the state vector."""
        return len(self.__info)

    def population_size(self):
        return self.popn_size

    def init(self, ctx, vec):
        """Initialise a state vector.

        :param ctx: The simulation context.
        :param vec: An uninitialised state vector of correct dimensions (see
            :py:func:`~state_size`).
        """
        self.popn_size = ctx.params['model']['population_size']
        self.__R0_lookup = None
        self.__external_lookup = None
        self.__regularise_R0_ix = ctx.params.get_chained(
            ['model', 'regularisation', 'R0_ix'], default=False)

        prior = ctx.params['model']['prior']
        rnd_size = vec[..., 0].shape
        rnd = ctx.component['random']['model']

        num_exps = 10.0
        vec[..., :] = 0
        vec[..., 0] = self.popn_size - num_exps
        vec[..., 1] = num_exps
        vec[..., self.ix_R0] = prior['R0'](rnd, size=rnd_size)
        vec[..., self.ix_sigma] = prior['sigma'](rnd, size=rnd_size)
        vec[..., self.ix_gamma] = prior['gamma'](rnd, size=rnd_size)
        vec[..., self.ix_t0] = prior['t0'](rnd, size=rnd_size)
        vec[..., self.ix_R0_ix] = 0
        vec[..., self.ix_R0_val] = 0

        self.load_samples_file(ctx, vec)
        self.load_lookup_tables(ctx)
        self.init_lookup_values(ctx, vec)

    def sample_columns(self):
        """Identify parameters that can be saved and loaded."""
        ix_tbl = {
            'R0': self.ix_R0,
            'sigma': self.ix_sigma,
            'gamma': self.ix_gamma,
            't0': self.ix_t0,
            'R0_ix': self.ix_R0_ix,
        }
        return ix_tbl

    def load_samples_file(self, ctx, vec):
        """Load initial parameter values from an external data file."""
        if 'prior_samples' not in ctx.params['model']:
            return

        logger = logging.getLogger(__name__)
        samples = ctx.params['model']['prior_samples']
        data_dir = Path(ctx.params['data_dir'])
        data_file = data_dir / samples['file']
        columns = [(name, np.float) for name in samples['columns']]

        tbl = pypfilt.io.read_table(data_file, columns)
        if tbl.shape != vec[..., 0].shape:
            raise ValueError('Incompatible data shapes: {} and {}'.format(
                vec[..., 0].shape, tbl.shape))

        ix_tbl = self.sample_columns()
        for name in samples['columns']:
            if name not in ix_tbl:
                raise ValueError('Unknown parameter {}'.format(name))

            ix = ix_tbl[name]
            vec[..., ix] = tbl[name]

            # NOTE: warn if sampled values exceed the parameter bounds.
            min_val = np.min(tbl[name])
            max_val = np.max(tbl[name])
            if min_val < ctx.params['model']['param_min'][ix]:
                logger.warning('Sampled value for {} outside bounds'
                               .format(name))
            elif max_val > ctx.params['model']['param_max'][ix]:
                logger.warning('Sampled value for {} outside bounds'
                               .format(name))
            # Clip the sampled values to enforce the parameter bounds.
            # The alternative is to leave the sample values as provided, in
            # which case they will only be clipped if post-regularisation is
            # enabled and the particles are resampled.
            vec[..., ix] = np.clip(vec[..., ix],
                                   ctx.params['model']['param_min'][ix],
                                   ctx.params['model']['param_max'][ix])

    def resume_from_cache(self, ctx):
        """
        A simulation will begin from a saved state, so the model must check
        whether any lookup tables are defined.

        :param ctx: The simulation context.
        """
        self.load_lookup_tables(ctx)

    def load_lookup_tables(self, ctx):
        """
        Allow R0 and imported cases to be provided via lookup tables.

        :param ctx: The simulation context.
        """
        logger = logging.getLogger(__name__)
        tables = ctx.component.get('lookup', {})

        # Check for the R0 lookup table.
        if 'R0' in tables:
            self.__R0_lookup = tables['R0']
            logger.info('Using lookup table for R0 with {} values'.format(
                self.__R0_lookup.value_count()))

        # Check for the external exposures lookup table.
        exp_table = 'external_exposures'
        if exp_table in tables:
            self.__external_lookup = tables[exp_table]
            logger.info(
                'Using lookup table for external exposures with {} values'
                .format(self.__external_lookup.value_count()))

    def init_lookup_values(self, ctx, vec):
        """
        Initialise the ``R0_ix`` values if an R0 lookup table is defined.

        :param ctx: The simulation context.
        :param vec: An uninitialised state vector of correct dimensions (see
            :py:func:`~state_size`).
        """
        if self.__R0_lookup is not None:
            num_values = self.__R0_lookup.value_count()
            if num_values > 1:
                rnd = ctx.component['random']['model']
                rnd_size = vec[..., 0].shape
                vec[..., self.ix_R0_ix] = rnd.integers(num_values,
                                                       size=rnd_size)
            else:
                vec[..., self.ix_R0_ix] = 0

    def update(self, ctx, step_date, dt, is_fs, prev, curr):
        """Perform a single time-step.

        :param ctx: The simulation context.
        :param step_date: The date and time of the current time-step.
        :param dt: The time-step size (days).
        :param is_fs: Indicates whether this is a forecasting simulation.
        :param prev: The state before the time-step.
        :param curr: The state after the time-step (destructively updated).
        """

        rnd = ctx.component['random']['model']
        params = ctx.params

        # Update parameters and lookup tables that are defined in self.init()
        # and which will not exist if we are resuming from a cached state.
        self.popn_size = ctx.params['model']['population_size']

        # Extract each parameter.
        R0 = prev[..., self.ix_R0].copy()
        sigma = prev[..., self.ix_sigma].copy()
        gamma = prev[..., self.ix_gamma].copy()
        t0 = prev[..., self.ix_t0].copy()
        R0_ix = np.around(prev[..., self.ix_R0_ix]).astype(int)

        if self.__R0_lookup is not None:
            start = ctx.component['time'].start
            forecast_with_future_R0 = False
            param_name = 'forecast_with_future_R0'
            if 'model' in params and param_name in params['model']:
                forecast_with_future_R0 = params['model'][param_name]
            if is_fs and not forecast_with_future_R0:
                # NOTE: Forecasting run, only using Reff(forecast_date).
                when = start
            else:
                when = step_date
            # Retrieve R0(t) values from the lookup table.
            R0_values = self.__R0_lookup.lookup(when)
            R0 = R0_values[R0_ix]

        beta = R0 * gamma

        external = np.zeros(beta.shape)
        if self.__external_lookup is not None:
            external_values = self.__external_lookup.lookup(step_date)
            n = len(external_values)
            if n == 1:
                external[:] = external_values[0]
            elif n == len(external):
                # NOTE: we currently assume that when there are multiple
                # external exposure trajectories, that the values will only be
                # non-zero in the forecasting period (i.e., there are no more
                # observations, so particles will not be resampled) and we can
                # simply assign the trajectories to each particle in turn.
                external[:] = external_values[:]
            else:
                raise ValueError('Invalid number of lookup values: {}'
                                 .format(n))

        epoch = ctx.component['time'].to_scalar(ctx.params['epoch'])
        curr_t = ctx.component['time'].to_scalar(step_date)
        zero_mask = t0 > (curr_t - epoch)
        R0[zero_mask] = 0
        beta[zero_mask] = 0
        sigma[zero_mask] = 0
        gamma[zero_mask] = 0

        # Extract each compartment.
        S = prev[..., self.ix_S].astype(int)
        E1 = prev[..., self.ix_E1].astype(int)
        E2 = prev[..., self.ix_E2].astype(int)
        I1 = prev[..., self.ix_I1].astype(int)
        I2 = prev[..., self.ix_I2].astype(int)

        # Calculate the rates at which an individual leaves each compartment.
        s_out_rate = dt * (beta * (I1 + I2) + external) / self.popn_size
        s_out_rate[S < 1] = 0
        e_out_rate = dt * 2 * sigma
        i_out_rate = dt * 2 * gamma

        # Calculate an individual's probability of leaving each compartment.
        s_out_prob = - np.expm1(- s_out_rate)
        e_out_prob = - np.expm1(- e_out_rate)
        i_out_prob = - np.expm1(- i_out_rate)

        # Sample the outflow rate for each compartment.
        s_out = rnd.binomial(S, s_out_prob)
        e1_out = rnd.binomial(E1, e_out_prob)
        e2_out = rnd.binomial(E2, e_out_prob)
        i1_out = rnd.binomial(I1, i_out_prob)
        i2_out = rnd.binomial(I2, i_out_prob)

        if (any(np.isinf(s_out_rate)) or any(np.isinf(s_out_prob))):
            print('S out rate: {} to {}'.format(np.min(s_out_rate),
                                                np.max(s_out_rate)))
            print('S out prob: {} to {}'.format(np.min(s_out_prob),
                                                np.max(s_out_prob)))
            print('S: {} to {}'.format(np.min(S), np.max(S)))
            print('S out: {} to {}'.format(np.min(s_out), np.max(s_out)))
            print('when:', when)
            print('dt:', dt)
            print('beta:', np.min(beta), np.max(beta))
            print('R0:', np.min(R0), np.max(R0))
            print('gamma:', np.min(gamma), np.max(gamma))
            print(np.max(dt * (beta * (I1 + I2))))
            print(np.max(dt * external / S))
            print(np.min(dt * (beta * (I1 + I2))))
            print(np.min(dt * external / S))
            raise ValueError('stop')

        # Update the compartment values.
        curr[..., self.ix_S] = S - s_out
        curr[..., self.ix_E1] = E1 + s_out - e1_out
        curr[..., self.ix_E2] = E2 + e1_out - e2_out
        curr[..., self.ix_I1] = I1 + e2_out - i1_out
        curr[..., self.ix_I2] = I2 + i1_out - i2_out

        # Calculate the size of the R compartment and clip appropriately.
        curr[..., self.ix_R] = np.clip(
            self.popn_size - np.sum(curr[..., :self.ix_R], axis=-1),
            0.0,
            self.popn_size)

        # Keep parameters fixed.
        curr[..., self.ix_R0:] = prev[..., self.ix_R0:]
        # Record the R0(t) values for each particle.
        curr[..., self.ix_R0_val] = R0

    def pr_inf(self, prev, curr):
        """
        Return the probability of an individual becoming infected, for any
        number of state vectors.

        :param prev: The model states at the start of the observation period.
        :param curr: The model states at the end of the observation period.
        """
        # Count the number of susceptible / exposed individuals at both ends
        # of the simulation period.
        prev_amt = np.sum(prev[..., :self.ix_I2], axis=-1)
        curr_amt = np.sum(curr[..., :self.ix_I2], axis=-1)
        # Avoid returning very small negative values (e.g., -1e-10).
        num_infs = np.maximum(prev_amt - curr_amt, 0)
        return num_infs / self.popn_size

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
        return np.ceil(1 - hist[..., self.ix_S])

    def is_extinct(self, hist):
        """
        Return an array that identifies state vectors where the epidemic has
        become extinct.

        By default, this method returns ``False`` for all particles.
        Stochastic models should override this method.

        :param hist: A matrix of arbitrary dimensions, whose final dimension
            covers the model state space (i.e., has a length no smaller than
            that returned by :py:func:`state_size`).
        :type hist: numpy.ndarray

        :returns: A matrix of one fewer dimensions than ``hist`` that contains
            ``True`` for state vectors where the epidemic is extinct and
            ``False`` for state vectors where the epidemic is ongoing.
        :rtype: numpy.ndarray
        """
        # Count the number of individuals in E1, E2, I1, and I2.
        num_exposed = np.sum(hist[..., self.ix_E1:self.ix_R], axis=-1)
        return num_exposed == 0

    def is_valid(self, hist):
        """Ignore state vectors where no infections have occurred, as their
        properties (such as parameter distributions) are uninformative."""
        return self.is_seeded(hist)

    def describe(self):
        descr = [info_tuple for info_tuple in self.__info]
        # Check whether R0_ix can be smoothed by, e.g., post-regularistion.
        if self.__regularise_R0_ix:
            for ix in range(len(descr)):
                if descr[ix][0] == 'R0_ix':
                    descr[ix] = (descr[ix][0], True, *descr[ix][2:])
        return descr

    def stat_info(self):
        """
        Return the summary statistics that are provided by this model.

        Each statistic is represented as a ``(name, stat_fn)`` tuple, where
        ``name`` is a string and ``stat_fn`` is a function that accepts one
        argument (the particle history matrix) and returns the statistic (see,
        e.g., :py:func:`stat_generation_interval`).
        """
        return [("gen_int", self.stat_generation_interval)]

    def stat_generation_interval(self, hist):
        """
        Calculate the mean generation interval for each particle.

        :param hist: The particle history matrix, or a subset thereof.
        """
        return 1 / hist[..., self.ix_sigma] + 0.75 / hist[..., self.ix_gamma]
