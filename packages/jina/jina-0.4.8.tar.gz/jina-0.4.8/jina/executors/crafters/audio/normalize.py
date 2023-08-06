__copyright__ = "Copyright (c) 2020 Jina AI Limited. All rights reserved."
__license__ = "Apache-2.0"

from typing import Dict

import numpy as np

from .. import BaseCrafter


class AudioNormalizer(BaseCrafter):
    """
    :class:`AudioNormalizer` normalizes the audio signal on doc-level.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def craft(self, blob: np.ndarray, *args, **kwargs) -> Dict:
        """
        Reads the `ndarray` of the audio signal, normalizes the signal and saves the `ndarray` of the normalized signal
        in the `blob` of the Document.

        :param blob: the ndarray of the audio signal
        :return: a Document dict with the normalized audio signal
        """
        import librosa
        signal_norm = librosa.util.normalize(blob)

        return dict(offset=0, weight=1., blob=signal_norm)
