import tensorflow as tf
import hyperchamber as hc
import hypergan as hg
import numpy as np
from hypergan.losses.category_loss import CategoryLoss
from hypergan.ops import TensorflowOps
from hypergan.multi_component import MultiComponent


from tests.mocks import MockDiscriminator, mock_gan
from unittest.mock import MagicMock

loss_config = {'test': True, 'reduce':'reduce_mean', 'labels': [0,1,0], 'categories': [3,4,3], 'category_lambda': 0.1, 'activation' : 'tanh'}

def build_gan():
    gan = mock_gan()
    gan.discriminator = MockDiscriminator(gan, {})
    loss = CategoryLoss(gan, loss_config)
    gan.loss = MultiComponent([gan.loss, loss])
    gan.create()
    return gan

class CategoryLossTest(tf.test.TestCase):

    def test_config(self):
        with self.test_session():
            self.gan = build_gan()
            loss = CategoryLoss(self.gan, loss_config)
            self.assertTrue(loss.config.test)

    def test_create(self):
        with self.test_session():
            self.gan = build_gan()
            d_loss, g_loss = loss.create()
            d_shape = loss.ops.shape(d_loss)
            g_shape = loss.ops.shape(g_loss)
            self.assertEqual(sum(d_shape), 1)
            self.assertEqual(sum(g_shape), 1)

if __name__ == "__main__":
    tf.test.main()
