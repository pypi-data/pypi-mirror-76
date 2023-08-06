import numpy as np


def constant(shape, value):
    return np.full(shape, value)


def uniform(shape, range=0.01, std=None, mean=0.0):
    """Sample initial weights from the uniform distribution.

    Parameters are sampled from U(a, b).

    Parameters
    ----------

    range: float or tuple
        When std is None then range determines a, b. If range is a float the
        weights are sampled from U(-range, range). If range is a tuple the
        weights are sampled from U(range[0], range[1]).

    std: float or None
        If std is a float then the weights are sampled from
        U(mean - np.sqrt(3) * std, mean + np.sqrt(3) * std).

    mean: float
        see std for description.
        :param shape:
    """
    if std is not None:
        a = mean - np.sqrt(3) * std
        b = mean + np.sqrt(3) * std
    elif hasattr(range, "__len__"):
        a, b = range  # range is a tuple
    else:
        a, b = -range, range  # range is a number
    return np.random.rand(*shape) * (b - a) + a


def normal(shape, mean=0.0, std=1.0):
    """Sample initial weights from the Gaussian distribution.

    Initial weight parameters are sampled from N(mean, std).

    Parameters
    ----------

    std: float
        Std of initial parameters.

    mean: float
        Mean of initial parameters.
        :param shape:

    """
    return np.random.randn(*shape) * std + mean


def orthogonal(shape, gain=1):
    assert len(shape) == 2
    if shape[0] == 1 and shape[1] == 1:
        return np.random.randn(1, 1) * gain

    a = np.random.randn(shape[0], shape[1])
    q, r = np.linalg.qr(a)
    # Make Q uniform
    d = np.diag(r)
    q *= np.sign(d)
    if shape[0] < shape[1]:
        q = q.T
    return gain * np.reshape(q, shape)


def _compute_fans(shape, in_axis, out_axis):
    fan_in = np.prod([shape[i] for i in in_axis])
    fan_out = np.prod([shape[i] for i in out_axis])
    return fan_in, fan_out


def variance_scaling(
    mode, shape, gain, distribution=normal, in_axis=None, out_axis=None
):
    """Variance Scaling initialization.
    """

    if in_axis is None:
        if len(shape) == 2:
            in_axis = [0]
        else:
            in_axis = list(range(1, len(shape)))

    if out_axis is None:
        out_axis = [i for i in range(len(shape)) if i not in in_axis]

    if len(shape) < 2:
        raise RuntimeError("This initializer only works with shapes of length >= 2")

    fan_in, fan_out = _compute_fans(shape, in_axis, out_axis)
    if mode == "fan_in":
        den = fan_in
    elif mode == "fan_out":
        den = fan_out
    elif mode == "fan_avg":
        den = (fan_in + fan_out) / 2.0
    else:
        raise ValueError(
            "mode must be fan_in, fan_out or fan_avg, value passed was {mode}"
        )
    std = gain * np.sqrt(1.0 / den)
    return distribution(shape, std=std)


def glorot_uniform(shape, gain=1, in_axis=None, out_axis=None):
    return glorot(shape, gain, uniform, in_axis, out_axis)


def glorot(shape, gain=1, distribution=normal, in_axis=None, out_axis=None):
    """Glorot weight initialization.

    This is also known as Xavier initialization [1]_.

    Parameters
    ----------

    initializer: lasagne.init.Initializer
        Initializer used to sample the weights, must accept `std` in its
        constructor to sample from a distribution with a given standard
        deviation.

    gain: float or 'relu'
        Scaling factor for the weights. Set this to ``1.0`` for linear and
        sigmoid units, to 'relu' or ``sqrt(2)`` for rectified linear units, and
        to ``sqrt(2/(1+alpha**2))`` for leaky rectified linear units with
        leakiness ``alpha``. Other transfer functions may need different
        factors.

    c01b: bool
        For a :class:`lasagne.layers.cuda_convnet.Conv2DCCLayer` constructed
        with ``dimshuffle=False``, `c01b` must be set to ``True`` to compute
        the correct fan-in and fan-out.

    References
    ----------

    .. [1] Xavier Glorot and Yoshua Bengio (2010):
           Understanding the difficulty of training deep feedforward neural
           networks. International conference on artificial intelligence and
           statistics.

    Notes
    -----

    For a :class:`DenseLayer <lasagne.layers.DenseLayer>`, if ``gain='relu'``
    and ``initializer=Uniform``, the weights are initialized as
    .. math::
       a &= \\sqrt{\\frac{12}{fan_{in}+fan_{out}}}\\\\
       W &\sim U[-a, a]
    If ``gain=1`` and ``initializer=Normal``, the weights are initialized as
    .. math::
       \\sigma &= \\sqrt{\\frac{2}{fan_{in}+fan_{out}}}\\\\
       W &\sim N(0, \\sigma)
       :param shape:
       :param distribution:
       :param in_axis:
       :param out_axis:
    """
    if len(shape) < 2:
        raise RuntimeError("This initializer only works with shapes of length >= 2")

    return variance_scaling(
        "fan_avg", shape, gain, distribution, in_axis=in_axis, out_axis=out_axis,
    )


def he(shape, gain=np.sqrt(2), distribution=normal, in_axis=None, out_axis=None):
    """He weight initialization.
    Weights are initialized with a standard deviation of
    :param shape:
    :param distribution:
    :param in_axis:
    :param out_axis:
    :math:`\\sigma = gain \\sqrt{\\frac{1}{fan_{in}}}` [1]_.

    Parameters
    ----------

    initializer : lasagne.init.Initializer
        Initializer used to sample the weights, must accept `std` in its
        constructor to sample from a distribution with a given standard
        deviation.

    gain : float or 'relu'
        Scaling factor for the weights. Set this to ``1.0`` for linear and
        sigmoid units, to 'relu' or ``sqrt(2)`` for rectified linear units, and
        to ``sqrt(2/(1+alpha**2))`` for leaky rectified linear units with
        leakiness ``alpha``. Other transfer functions may need different
        factors.

    c01b : bool
        For a :class:`lasagne.layers.cuda_convnet.Conv2DCCLayer` constructed
        with ``dimshuffle=False``, `c01b` must be set to ``True`` to compute
        the correct fan-in and fan-out.

    References
    ----------

    .. [1] Kaiming He et al. (2015):
           Delving deep into rectifiers: Surpassing human-level performance on
           imagenet classification. arXiv preprint arXiv:1502.01852.

    See Also
    ----------

    HeNormal  : Shortcut with Gaussian initializer.
    HeUniform : Shortcut with uniform initializer.
    """
    return variance_scaling(
        "fan_in", shape, gain, distribution, in_axis=in_axis, out_axis=out_axis
    )


def lecun(shape, gain=1.0, distribution=normal, in_axis=None, out_axis=None):
    """LeCun weight initialization.
    Weights are initialized with a standard deviation of
    :math:`\\sigma = gain \\sqrt{\\frac{1}{fan_{in}}}`.
   """
    return variance_scaling(
        "fan_in", shape, gain, distribution, in_axis=in_axis, out_axis=out_axis
    )
