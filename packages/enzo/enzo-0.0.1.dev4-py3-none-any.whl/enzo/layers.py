import numpy as np
from . import activations


class DenseLayer:
    """TODO: add desc, allow implicit input_length, finish docs

    Parameters
    ----------
    input_length : int
        The length of the vector of inputs this layer will receive. For hidden layers,
        this is the number of units in the previous layer.
    n_units : int
        The number of neurons in the layer.
    activation : callable
        The activation function for this layer.

    Notes
    -----
    The weights matrix (``self.weights``) has each column corresponding to one unit's
    weights. This allows forward propagation with a matrix where each row is one sample
    to be ``__matmul__``-ed with ``self.weights`` to generate activations.
    """

    def __init__(self, input_length, n_units, activation=None):
        if activation is None:
            activation = activations.relu
        self.weights = np.random.rand(input_length + 1, n_units)
        self.input_length = input_length
        self.n_units = n_units
        self.activation = activation
        self.outputs = None

    @staticmethod
    def _append_column_of_ones(samples):
        """Prepare matrix of samples for multiplication with a matrix of weights.

        This allows for the bias to be taken into account.
        """
        n_samples = len(samples)
        return np.append(samples, np.ones(n_samples).reshape(n_samples, 1), axis=1)

    def forward(self, samples):
        """Return and store in ``self.outputs`` the activation matrix of this layer
            after forward propagation.
        """
        pre_actiation_func = DenseLayer._append_column_of_ones(samples) @ self.weights
        self.outputs = self.activation(pre_actiation_func)
        return self.outputs
