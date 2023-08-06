"""Layers for sequential models"""

from abc import ABC
from abc import abstractmethod
import numpy as np
from . import activations
from .exceptions import LayerBuildingError


class Layer(ABC):
    """Parent class for all custom layers.

    Subclasses must implement :func:`build`.
    """

    @abstractmethod
    def build(self, input_length):
        """Initiate weights and other attributes that depend on `input_length`

        Parameters
        ----------
        input_length : int
            The shape of inputs to this layer (samples).
        """


class DenseLayer(Layer):
    """A densely connected layer for neural networks.

    Parameters
    ----------
    n_units : int
        The number of neurons in the layer.
    activation : callable, optional
        The activation function for this layer. Default :func:`enzo.activations.relu`
    input_length : int, optional
        The length of the vector of inputs this layer will receive. For hidden layers,
        this should the number of units in the previous layer.
        :class:`enzo.models.Model` automatically defines `input_length` for all layers
        excluding the first.

    Notes
    -----
    The weights matrix (`self.weights`) has each column corresponding to one unit's
    weights. This allows forward propagation with a matrix where each row is one sample
    to be `__matmul__`-ed with `self.weights` to generate activations.
    """

    def __init__(self, n_units, activation=None, input_length=None):
        self.n_units = n_units
        self.activation = activation
        self.output_length = n_units
        self.input_length = input_length
        if activation is None:
            self.activation = activations.relu
        self.weights = None
        self.outputs = None

    @staticmethod
    def _append_column_of_ones(samples):
        """Prepare matrix of samples for multiplication with a matrix of weights.

        This allows for the bias to be taken into account.
        """
        return np.append(samples, np.ones((len(samples), 1)), axis=1)

    @staticmethod
    def _shape_samples(samples):
        try:
            ndim = samples.ndim
        except AttributeError:
            samples = np.array(samples)
            ndim = samples.ndim
        if ndim == 1:
            return samples.reshape(1, len(samples))
        if ndim == 2:
            return samples
        raise ValueError(f"Samples must be 1- or 2-dimensional (not {samples.ndim}-)")

    @staticmethod
    def _prepare_samples(samples):
        samples = DenseLayer._shape_samples(samples)
        return DenseLayer._append_column_of_ones(samples)

    def forward(self, samples):
        """Return and store in `self.outputs` the activation matrix of this layer
            after forward propagation.
        """
        samples = DenseLayer._prepare_samples(samples)
        pre_actiation_func = samples @ self.weights
        self.outputs = self.activation(pre_actiation_func)
        return self.outputs

    def build(self, input_length=None):
        """Initialize the weights of this :class:`DenseLayer`.

        Parameters
        ----------
        input_length : int
            The shape of inputs to this layer (samples).
        """
        if input_length is None:
            input_length = self.input_length
        elif input_length != self.input_length and self.input_length is not None:
            raise LayerBuildingError(
                "input_length doesn't match input_length from initialization"
            )
        self.weights = np.random.rand(input_length + 1, self.n_units)
