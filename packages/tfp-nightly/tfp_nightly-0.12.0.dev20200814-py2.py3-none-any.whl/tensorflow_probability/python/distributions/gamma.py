# Copyright 2018 The TensorFlow Probability Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
"""The Gamma distribution class."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Dependency imports
import numpy as np
import tensorflow.compat.v2 as tf

from tensorflow_probability.python.bijectors import softplus as softplus_bijector
from tensorflow_probability.python.distributions import distribution
from tensorflow_probability.python.distributions import kullback_leibler
from tensorflow_probability.python.internal import assert_util
from tensorflow_probability.python.internal import batched_rejection_sampler as brs
from tensorflow_probability.python.internal import custom_gradient as tfp_custom_gradient
from tensorflow_probability.python.internal import distribution_util
from tensorflow_probability.python.internal import dtype_util
from tensorflow_probability.python.internal import implementation_selection
from tensorflow_probability.python.internal import prefer_static as ps
from tensorflow_probability.python.internal import reparameterization
from tensorflow_probability.python.internal import samplers
from tensorflow_probability.python.internal import tensor_util
from tensorflow_probability.python.internal import tensorshape_util

__all__ = [
    'Gamma',
]


class Gamma(distribution.Distribution):
  """Gamma distribution.

  The Gamma distribution is defined over positive real numbers using
  parameters `concentration` (aka "alpha") and `rate` (aka "beta").

  #### Mathematical Details

  The probability density function (pdf) is,

  ```none
  pdf(x; alpha, beta, x > 0) = x**(alpha - 1) exp(-x beta) / Z
  Z = Gamma(alpha) beta**(-alpha)
  ```

  where:

  * `concentration = alpha`, `alpha > 0`,
  * `rate = beta`, `beta > 0`,
  * `Z` is the normalizing constant, and,
  * `Gamma` is the [gamma function](
    https://en.wikipedia.org/wiki/Gamma_function).

  The cumulative density function (cdf) is,

  ```none
  cdf(x; alpha, beta, x > 0) = GammaInc(alpha, beta x) / Gamma(alpha)
  ```

  where `GammaInc` is the [lower incomplete Gamma function](
  https://en.wikipedia.org/wiki/Incomplete_gamma_function).

  The parameters can be intuited via their relationship to mean and stddev,

  ```none
  concentration = alpha = (mean / stddev)**2
  rate = beta = mean / stddev**2 = concentration / mean
  ```

  Distribution parameters are automatically broadcast in all functions; see
  examples for details.

  Warning: The samples of this distribution are always non-negative. However,
  the samples that are smaller than `np.finfo(dtype).tiny` are rounded
  to this value, so it appears more often than it should.
  This should only be noticeable when the `concentration` is very small, or the
  `rate` is very large. See note in `tf.random.gamma` docstring.

  Samples of this distribution are reparameterized (pathwise differentiable).
  The derivatives are computed using the approach described in the paper

  [Michael Figurnov, Shakir Mohamed, Andriy Mnih.
  Implicit Reparameterization Gradients, 2018](https://arxiv.org/abs/1805.08498)

  #### Examples

  ```python
  import tensorflow_probability as tfp
  tfd = tfp.distributions

  dist = tfd.Gamma(concentration=3.0, rate=2.0)
  dist2 = tfd.Gamma(concentration=[3.0, 4.0], rate=[2.0, 3.0])
  ```

  Compute the gradients of samples w.r.t. the parameters:

  ```python
  concentration = tf.constant(3.0)
  rate = tf.constant(2.0)
  dist = tfd.Gamma(concentration, rate)
  samples = dist.sample(5)  # Shape [5]
  loss = tf.reduce_mean(tf.square(samples))  # Arbitrary loss function
  # Unbiased stochastic gradients of the loss function
  grads = tf.gradients(loss, [concentration, rate])
  ```

  """

  def __init__(self,
               concentration,
               rate,
               validate_args=False,
               allow_nan_stats=True,
               name='Gamma'):
    """Construct Gamma with `concentration` and `rate` parameters.

    The parameters `concentration` and `rate` must be shaped in a way that
    supports broadcasting (e.g. `concentration + rate` is a valid operation).

    Args:
      concentration: Floating point tensor, the concentration params of the
        distribution(s). Must contain only positive values.
      rate: Floating point tensor, the inverse scale params of the
        distribution(s). Must contain only positive values.
      validate_args: Python `bool`, default `False`. When `True` distribution
        parameters are checked for validity despite possibly degrading runtime
        performance. When `False` invalid inputs may silently render incorrect
        outputs.
      allow_nan_stats: Python `bool`, default `True`. When `True`, statistics
        (e.g., mean, mode, variance) use the value "`NaN`" to indicate the
        result is undefined. When `False`, an exception is raised if one or
        more of the statistic's batch members are undefined.
      name: Python `str` name prefixed to Ops created by this class.

    Raises:
      TypeError: if `concentration` and `rate` are different dtypes.
    """
    parameters = dict(locals())
    with tf.name_scope(name) as name:
      dtype = dtype_util.common_dtype(
          [concentration, rate], dtype_hint=tf.float32)
      self._concentration = tensor_util.convert_nonref_to_tensor(
          concentration, dtype=dtype, name='concentration')
      self._rate = tensor_util.convert_nonref_to_tensor(
          rate, dtype=dtype, name='rate')

      super(Gamma, self).__init__(
          dtype=dtype,
          validate_args=validate_args,
          allow_nan_stats=allow_nan_stats,
          reparameterization_type=reparameterization.FULLY_REPARAMETERIZED,
          parameters=parameters,
          name=name)

  @staticmethod
  def _param_shapes(sample_shape):
    return dict(
        zip(('concentration', 'rate'),
            ([tf.convert_to_tensor(sample_shape, dtype=tf.int32)] * 2)))

  @classmethod
  def _params_event_ndims(cls):
    return dict(concentration=0, rate=0)

  @property
  def concentration(self):
    """Concentration parameter."""
    return self._concentration

  @property
  def rate(self):
    """Rate parameter."""
    return self._rate

  def _batch_shape_tensor(self, concentration=None, rate=None):
    return ps.broadcast_shape(
        ps.shape(
            self.concentration if concentration is None else concentration),
        ps.shape(self.rate if rate is None else rate))

  def _batch_shape(self):
    return tf.broadcast_static_shape(
        self.concentration.shape,
        self.rate.shape)

  def _event_shape_tensor(self):
    return tf.constant([], dtype=tf.int32)

  def _event_shape(self):
    return tf.TensorShape([])

  @distribution_util.AppendDocstring(
      """Note: See `tf.random.gamma` docstring for sampling details and
      caveats.""")
  def _sample_n(self, n, seed=None):
    seed = samplers.sanitize_seed(seed, salt='gamma')

    return random_gamma(
        shape=ps.convert_to_shape_tensor([n]),
        concentration=tf.convert_to_tensor(self.concentration, self.dtype),
        rate=tf.convert_to_tensor(self.rate, self.dtype), seed=seed)

  def _log_prob(self, x, concentration=None, rate=None):
    concentration = tf.convert_to_tensor(
        self.concentration if concentration is None else concentration)
    rate = tf.convert_to_tensor(self.rate if rate is None else rate)
    log_unnormalized_prob = tf.math.xlogy(concentration - 1., x) - rate * x
    log_normalization = (tf.math.lgamma(concentration) -
                         concentration * tf.math.log(rate))
    return log_unnormalized_prob - log_normalization

  def _cdf(self, x):
    # Note that igamma returns the regularized incomplete gamma function,
    # which is what we want for the CDF.
    return tf.math.igamma(self.concentration, self.rate * x)

  def _entropy(self):
    concentration = tf.convert_to_tensor(self.concentration)
    return (concentration - tf.math.log(self.rate) +
            tf.math.lgamma(concentration) +
            ((1. - concentration) * tf.math.digamma(concentration)))

  def _mean(self):
    return self.concentration / self.rate

  def _variance(self):
    return self.concentration / tf.square(self.rate)

  def _stddev(self):
    return tf.sqrt(self.concentration) / self.rate

  @distribution_util.AppendDocstring(
      """The mode of a gamma distribution is `(shape - 1) / rate` when
      `shape > 1`, and `NaN` otherwise. If `self.allow_nan_stats` is `False`,
      an exception will be raised rather than returning `NaN`.""")
  def _mode(self):
    concentration = tf.convert_to_tensor(self.concentration)
    rate = tf.convert_to_tensor(self.rate)
    mode = (concentration - 1.) / rate
    if self.allow_nan_stats:
      assertions = []
    else:
      assertions = [assert_util.assert_less(
          tf.ones([], self.dtype), concentration,
          message='Mode not defined when any concentration <= 1.')]
    with tf.control_dependencies(assertions):
      return tf.where(
          concentration > 1.,
          mode,
          dtype_util.as_numpy_dtype(self.dtype)(np.nan))

  def _default_event_space_bijector(self):
    return softplus_bijector.Softplus(validate_args=self.validate_args)

  def _sample_control_dependencies(self, x):
    assertions = []
    if not self.validate_args:
      return assertions
    assertions.append(assert_util.assert_non_negative(
        x, message='Sample must be non-negative.'))
    return assertions

  def _parameter_control_dependencies(self, is_init):
    if not self.validate_args:
      return []
    assertions = []
    if is_init != tensor_util.is_ref(self.concentration):
      assertions.append(assert_util.assert_positive(
          self.concentration,
          message='Argument `concentration` must be positive.'))
    if is_init != tensor_util.is_ref(self.rate):
      assertions.append(assert_util.assert_positive(
          self.rate,
          message='Argument `rate` must be positive.'))
    return assertions


@kullback_leibler.RegisterKL(Gamma, Gamma)
def _kl_gamma_gamma(g0, g1, name=None):
  """Calculate the batched KL divergence KL(g0 || g1) with g0 and g1 Gamma.

  Args:
    g0: Instance of a `Gamma` distribution object.
    g1: Instance of a `Gamma` distribution object.
    name: Python `str` name to use for created operations.
      Default value: `None` (i.e., `'kl_gamma_gamma'`).

  Returns:
    kl_gamma_gamma: `Tensor`. The batchwise KL(g0 || g1).
  """
  with tf.name_scope(name or 'kl_gamma_gamma'):
    # Result from:
    #   http://www.fil.ion.ucl.ac.uk/~wpenny/publications/densities.ps
    # For derivation see:
    #   http://stats.stackexchange.com/questions/11646/kullback-leibler-divergence-between-two-gamma-distributions   pylint: disable=line-too-long
    g0_concentration = tf.convert_to_tensor(g0.concentration)
    g0_rate = tf.convert_to_tensor(g0.rate)
    g1_concentration = tf.convert_to_tensor(g1.concentration)
    g1_rate = tf.convert_to_tensor(g1.rate)
    return (((g0_concentration - g1_concentration) *
             tf.math.digamma(g0_concentration)) +
            tf.math.lgamma(g1_concentration) -
            tf.math.lgamma(g0_concentration) +
            g1_concentration * tf.math.log(g0_rate) -
            g1_concentration * tf.math.log(g1_rate) + g0_concentration *
            (g1_rate / g0_rate - 1.))


def _random_gamma_cpu(
    shape,
    concentration,
    rate,
    seed=None):
  """Sample using *fast* `tf.random.stateless_gamma`."""
  bad_concentration = (concentration <= 0.) | tf.math.is_nan(concentration)
  clipped_concentration = tf.where(
      bad_concentration,
      dtype_util.as_numpy_dtype(rate.dtype)(100.), concentration)
  bad_rate = (rate <= 0.) | tf.math.is_nan(rate)
  clipped_rate = tf.where(
      bad_rate,
      dtype_util.as_numpy_dtype(rate.dtype)(100.), rate)
  samples = tf.random.stateless_gamma(
      shape=shape, seed=seed, alpha=clipped_concentration,
      beta=clipped_rate, dtype=concentration.dtype)
  return tf.where(
      bad_rate | bad_concentration,
      dtype_util.as_numpy_dtype(rate.dtype)(np.nan), samples)


def _random_gamma_noncpu(
    shape,
    concentration,
    rate,
    seed=None):
  """Sample using XLA-friendly python-based rejection sampler."""
  return random_gamma_rejection(
      sample_shape=shape, alpha=concentration, beta=rate, seed=seed)


# tf.function required to access Grappler's implementation_selector.
@implementation_selection.never_runs_functions_eagerly
# TODO(b/163029794): Shape relaxation breaks XLA.
@tf.function(autograph=False, experimental_relax_shapes=False)
def _random_gamma_no_gradient(shape, concentration, rate, seed):
  """Sample a gamma, CPU specialized to stateless_gamma.

  Args:
    shape: Sample shape.
    concentration: Concentration of gamma distribution.
    rate: Rate parameter of gamma distribution.
    seed: int or Tensor seed.

  Returns:
    samples: Samples from gamma distributions.
  """
  seed = samplers.sanitize_seed(seed)

  sampler_impl = implementation_selection.implementation_selecting(
      fn_name='gamma',
      default_fn=_random_gamma_noncpu,
      cpu_fn=_random_gamma_cpu)
  return sampler_impl(
      shape=shape, concentration=concentration, rate=rate, seed=seed)


def _random_gamma_fwd(shape, concentration, rate, seed):
  """Compute output, aux (collaborates with _random_gamma_bwd)."""
  samples, impl = _random_gamma_no_gradient(shape, concentration, rate, seed)
  return (samples, impl), (samples, shape, concentration, rate)


def _random_gamma_bwd(aux, g):
  """The gradient of the gamma samples."""
  samples, shape, concentration, rate = aux
  dsamples, dimpl = g
  # Ignore any gradient contributions that come from the implementation enum.
  del dimpl
  partial_concentration = tf.raw_ops.RandomGammaGrad(
      alpha=concentration, sample=samples * rate) / rate
  partial_rate = -samples / rate
  # These will need to be shifted by the extra dimensions added from
  # `sample_shape`.
  reduce_dims = tf.range(tf.size(shape) - tf.maximum(tf.rank(concentration),
                                                     tf.rank(rate)))
  grad_concentration = tf.math.reduce_sum(
      dsamples * partial_concentration, axis=reduce_dims)
  grad_rate = tf.math.reduce_sum(dsamples * partial_rate, axis=reduce_dims)
  if (tensorshape_util.is_fully_defined(concentration.shape) and
      tensorshape_util.is_fully_defined(rate.shape) and
      concentration.shape == rate.shape):
    return grad_concentration, grad_rate, None  # seed=None

  ax_conc, ax_rate = tf.raw_ops.BroadcastGradientArgs(
      s0=tf.shape(concentration), s1=tf.shape(rate))
  grad_concentration = tf.reshape(
      tf.math.reduce_sum(grad_concentration, axis=ax_conc),
      tf.shape(concentration))
  grad_rate = tf.reshape(
      tf.math.reduce_sum(grad_rate, axis=ax_rate), tf.shape(rate))

  return grad_concentration, grad_rate, None  # seed=None


def _random_gamma_jvp(shape, primals, tangents):
  """Computes JVP for gamma sample (supports JAX custom derivative)."""
  concentration, rate, seed = primals
  dconcentration, drate, dseed = tangents
  del dseed
  # TODO(https://github.com/google/jax/issues/3768): eliminate broadcast_to?
  dconcentration = tf.broadcast_to(dconcentration, shape)
  drate = tf.broadcast_to(drate, shape)

  samples, impl = _random_gamma_no_gradient(shape, concentration, rate, seed)

  partial_concentration = tf.raw_ops.RandomGammaGrad(
      alpha=concentration, sample=samples * rate) / rate
  partial_rate = -samples / rate

  return (
      (samples, impl),
      (partial_concentration * dconcentration + partial_rate * drate,
       tf.zeros_like(impl)))


@tfp_custom_gradient.custom_gradient(
    vjp_fwd=_random_gamma_fwd,
    vjp_bwd=_random_gamma_bwd,
    jvp_fn=_random_gamma_jvp,
    nondiff_argnums=(0,))
def _random_gamma_gradient(shape, concentration, rate, seed):
  return _random_gamma_no_gradient(shape, concentration, rate, seed)


# TF custom_gradient doesn't support kwargs, so we wrap _random_gamma_gradient.
def random_gamma_with_runtime(shape, concentration, rate=None, seed=None):
  """Returns both a sample and the id of the implementation-selected runtime."""
  # This method exists chiefly for testing purposes.
  dtype = dtype_util.common_dtype([concentration, rate], tf.float32)
  concentration = tf.convert_to_tensor(concentration, dtype=dtype)
  rate = tf.convert_to_tensor(1. if rate is None else rate, dtype=dtype)
  shape = ps.convert_to_shape_tensor(shape, dtype_hint=tf.int32, name='shape')

  total_shape = ps.concat(
      [shape, ps.broadcast_shape(ps.shape(concentration), ps.shape(rate))],
      axis=0)
  seed = samplers.sanitize_seed(seed, salt='random_gamma')
  return _random_gamma_gradient(total_shape, concentration, rate, seed)


def random_gamma(shape, concentration, rate=None, seed=None):
  return random_gamma_with_runtime(shape, concentration, rate, seed=seed)[0]


def random_gamma_rejection(
    sample_shape, alpha, beta=None, log_beta=None, internal_dtype=tf.float64,
    seed=None, log_space=False):
  """Samples from the gamma distribution.

  The sampling algorithm is rejection sampling [1], and pathwise gradients with
  respect to alpha are computed via implicit differentiation [2].

  Args:
    sample_shape: The output sample shape. Must broadcast with both
      `alpha` and `beta`.
    alpha: Floating point tensor, the alpha params of the
      distribution(s). Must contain only positive values. Must broadcast with
      `beta`.
    beta: Floating point tensor, the inverse scale params of the
      distribution(s). Must contain only positive values. Must broadcast with
      `alpha`. If `None`, handled as if 1 (but possibly more efficiently).
       Mutually exclusive with `log_beta`.
    log_beta: Floating point tensor, log of the inverse scale params of the
      distribution(s). Must broadcast with `alpha`. If `None`, handled as if 0
      (but possibly more efficiently). Mutually exclusive with `beta`.
    internal_dtype: dtype to use for internal computations.
    seed: (optional) The random seed.
    log_space: Optionally sample log(gamma) variates.

  Returns:
    Differentiable samples from the gamma distribution.

  #### References

  [1] George Marsaglia and Wai Wan Tsang. A simple method for generating Gamma
      variables. ACM Transactions on Mathematical Software, 2000.

  [2] Michael Figurnov, Shakir Mohamed, and Andriy Mnih. Implicit
      Reparameterization Gradients. Neural Information Processing Systems, 2018.
  """
  generate_and_test_samples_seed, alpha_fix_seed = samplers.split_seed(
      seed, salt='random_gamma')
  output_dtype = dtype_util.common_dtype([alpha, beta, log_beta],
                                         dtype_hint=tf.float32)

  def rejection_sample(alpha):
    """Gamma rejection sampler."""
    # Note that alpha here already has a shape that is broadcast with beta.
    cast_alpha = tf.cast(alpha, internal_dtype)

    good_params_mask = (alpha > 0.)
    # When replacing NaN values, use 100. for alpha, since that leads to a
    # high-likelihood of the rejection sampler accepting on the first pass.
    safe_alpha = tf.where(good_params_mask, cast_alpha, 100.)

    modified_safe_alpha = tf.where(
        safe_alpha < 1., safe_alpha + 1., safe_alpha)

    one_third = tf.constant(1. / 3, dtype=internal_dtype)
    d = modified_safe_alpha - one_third
    c = one_third * tf.math.rsqrt(d)

    def generate_and_test_samples(seed):
      """Generate and test samples."""
      v_seed, u_seed = samplers.split_seed(seed)

      def generate_positive_v():
        """Generate positive v."""
        def _inner(seed):
          x = samplers.normal(
              sample_shape, dtype=internal_dtype, seed=seed)
          # This implicitly broadcasts alpha up to sample shape.
          v = 1 + c * x
          return (x, v), v > 0.

        # Note: It should be possible to remove this 'inner' call to
        # `batched_las_vegas_algorithm` and merge the v > 0 check into the
        # overall check for a good sample. This would lead to a slightly simpler
        # implementation; it is unclear whether it would be faster. We include
        # the inner loop so this implementation is more easily comparable to
        # Ref. [1] and other implementations.
        return brs.batched_las_vegas_algorithm(_inner, v_seed)[0]

      (x, v) = generate_positive_v()
      logv = tf.math.log1p(c * x)
      x2 = x * x
      v3 = v * v * v
      logv3 = logv * 3

      u = samplers.uniform(
          sample_shape, dtype=internal_dtype, seed=u_seed)

      # In [1], the suggestion is to first check u < 1 - 0.331 * x2 * x2, and to
      # run the check below only if it fails, in order to avoid the relatively
      # expensive logarithm calls. Our algorithm operates in batch mode: we will
      # have to compute or not compute the logarithms for the entire batch, and
      # as the batch gets larger, the odds we compute it grow. Therefore we
      # don't bother with the "cheap" check.
      good_sample_mask = tf.math.log(u) < (x2 / 2. + d * (1 - v3 + logv3))

      return logv3 if log_space else v3, good_sample_mask

    samples = brs.batched_las_vegas_algorithm(
        generate_and_test_samples, seed=generate_and_test_samples_seed)[0]

    alpha_fix_unif = samplers.uniform(  # in [0, 1)
        sample_shape, dtype=internal_dtype, seed=alpha_fix_seed)

    if log_space:
      alpha_lt_one_fix = tf.where(
          safe_alpha < 1.,
          # Why do we use log1p(-x)? x is in [0, 1) and log(0) = -inf, is bad.
          # x ~ U(0,1) => 1-x ~ U(0,1)
          # But at the boundary, 1-x in (0, 1]. Good.
          # So we can take log(unif(0,1)) safely as log(1-unif(0,1)).
          # log1p(-0) = 0, and log1p(-almost_one) = -not_quite_inf. Good.
          tf.math.log1p(-alpha_fix_unif) / safe_alpha,
          tf.zeros((), dtype=internal_dtype))
      samples = samples + tf.math.log(d) + alpha_lt_one_fix
    else:
      alpha_lt_one_fix = tf.where(
          safe_alpha < 1.,
          tf.math.pow(alpha_fix_unif, tf.math.reciprocal(safe_alpha)),
          tf.ones((), dtype=internal_dtype))
      samples = samples * d * alpha_lt_one_fix

    samples = tf.where(good_params_mask, samples, np.nan)
    output_type_samples = tf.cast(samples, output_dtype)

    return output_type_samples

  broadcast_alpha_shape = ps.broadcast_shape(
      ps.shape(alpha), ps.shape(1 if beta is None else beta))
  broadcast_alpha = tf.broadcast_to(alpha, broadcast_alpha_shape)
  alpha_samples = rejection_sample(broadcast_alpha)

  if beta is not None and log_beta is not None:
    raise ValueError('`beta` and `log_beta` are mutually exclusive.')

  def fix_zero_samples(s):
    if log_space:
      return s
    # We use `tf.where` instead of `tf.maximum` because we need to allow for
    # `samples` to be `nan`, but `tf.maximum(nan, x) == x`.
    return tf.where(
        s == 0, np.finfo(dtype_util.as_numpy_dtype(s.dtype)).tiny, s)

  if beta is None and log_beta is None:
    return fix_zero_samples(alpha_samples)

  if log_space:
    if log_beta is None:
      log_beta = tf.math.log(tf.where(beta > 0., beta, np.nan))
    return alpha_samples - log_beta
  else:
    if beta is None:
      beta = tf.math.exp(log_beta)
    corrected_beta = tf.where(beta > 0., beta, np.nan)  # log_beta=-inf case
    return fix_zero_samples(alpha_samples / corrected_beta)
