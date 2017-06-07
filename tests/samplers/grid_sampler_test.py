import tensorflow as tf
import hypergan as hg
import hyperchamber as hc
import numpy as np

from hypergan.samplers.grid_sampler import GridSampler
from hypergan.gan_component import ValidationException
from hypergan.ops import TensorflowOps
from tests.mocks import mock_gan

class GridSamplerTest(tf.test.TestCase):
    def test_config(self):
        with self.test_session():
            gan = mock_gan()
            gan.create()

            sampler = GridSampler(gan)
            self.assertEqual(sampler.sample('/tmp/test.png')[0]['image'].shape[-1], 1)

if __name__ == "__main__":
    tf.test.main()
