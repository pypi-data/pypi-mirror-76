__copyright__ = "Copyright (c) 2020 Jina AI Limited. All rights reserved."
__license__ = "Apache-2.0"

import numpy as np

from .. import BaseNumericEncoder
from ...decorators import batching

class FitTransformEncoder(BaseNumericEncoder):
    """
    :class:`FitTransformEncoder` encodes data from an ndarray in size `B x T` into an ndarray in size `B x D`
    Parent class for RandomGaussianEncoder, RandomSparseEncoder and TSNEEncoder to prevent redundant code
    """

    def __init__(self,
                 output_dim: int,
                 random_state=2020,
                 *args,
                 **kwargs):
        """
        :param output_dim: the output size.
        """
        super().__init__(*args, **kwargs)
        self.output_dim = output_dim
        self.random_state = random_state

    @batching
    def encode(self, data: 'np.ndarray', *args, **kwargs) -> 'np.ndarray':
        """
        :param data: a `B x T` numpy ``ndarray``, `B` is the size of the batch
        :return: a `B x D` numpy ``ndarray``
        """
        return self.model.fit_transform(data)


class RandomGaussianEncoder(FitTransformEncoder):
    """
    :class:`RandomGaussianEncoder` encodes data from an ndarray in size `B x T` into an ndarray in size `B x D`
    https://scikit-learn.org/stable/modules/generated/sklearn.random_projection.GaussianRandomProjection.html
    """
    def post_init(self):
        from sklearn.random_projection import GaussianRandomProjection
        self.model = GaussianRandomProjection(n_components=self.output_dim, random_state=self.random_state)


class RandomSparseEncoder(FitTransformEncoder):
    """
    :class:`RandomSparseEncoder` encodes data from an ndarray in size `B x T` into an ndarray in size `B x D`
    https://scikit-learn.org/stable/modules/generated/sklearn.random_projection.SparseRandomProjection.html
    """
    def post_init(self):
        from sklearn.random_projection import SparseRandomProjection
        self.model = SparseRandomProjection(n_components=self.output_dim, random_state=self.random_state)


class TSNEEncoder(FitTransformEncoder):
    """
    :class:`TSNEEncoder` encodes data from an ndarray in size `B x T` into an ndarray in size `B x D`.
    https://scikit-learn.org/stable/modules/generated/sklearn.manifold.TSNE.html
    """
    def post_init(self):
        from sklearn.manifold import TSNE
        self.model = TSNE(n_components=self.output_dim, random_state=self.random_state)


class FeatureAgglomerationEncoder(FitTransformEncoder):
    """
    :class:`FeatureAgglomerationEncoder` encodes data from an ndarray in size `B x T` into an ndarray in size `B x D`
    https://scikit-learn.org/stable/modules/generated/sklearn.cluster.FeatureAgglomeration.html
    """
    def post_init(self):
        from sklearn.cluster import FeatureAgglomeration
        self.model = FeatureAgglomeration(n_clusters=self.output_dim)
