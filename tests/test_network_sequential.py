#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unittest

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import tensorflow as tf
import tensorlayer as tl

from tensorlayer.decorators import private_method

try:
    from tests.unittests_helper import CustomTestCase
except ImportError:
    from unittests_helper import CustomTestCase


class Network_Sequential_Test(CustomTestCase):

    @classmethod
    def setUpClass(cls):

        with tf.variable_scope("test_scope"):
            cls.model = tl.networks.Sequential(name="My_Seq_net")

            cls.model.add(tl.layers.DenseLayer(n_units=100, act=tf.nn.relu, name="seq_layer_1"))
            cls.model.add(tl.layers.DenseLayer(n_units=200, act=tf.nn.relu, name="seq_layer_2"))
            cls.model.add(tl.layers.DenseLayer(n_units=300, act=tf.nn.relu, name="seq_layer_4"))
            cls.model.add(tl.layers.DenseLayer(n_units=400, act=tf.nn.relu, name="seq_layer_5"))
            cls.model.add(tl.layers.DenseLayer(n_units=500, act=tf.nn.relu, name="seq_layer_6"))

            plh = tf.placeholder(tf.float16, (100, 32))

            cls.train_model = cls.model.compile(plh, reuse=False, is_train=True)
            cls.test_model = cls.model.compile(plh, reuse=True, is_train=False)

    def test_get_all_param_tensors(self):
        n_weight_tensors = len(self.model.get_all_params())
        tl.logging.debug("# Weight Tensors: %d" % n_weight_tensors)

        self.assertEqual(n_weight_tensors, 10)

    def test_count_params(self):
        n_params = self.model.count_params()
        tl.logging.debug("# Parameters: %d" % n_params)

        self.assertEqual(n_params, 404700)

    def test__getitem__(self):

        with self.assertNotRaises(Exception):

            layer = self.model["seq_layer_1"]
            self.assertTrue(isinstance(layer, tl.layers.DenseLayer))

    def test_network_output(self):
        self.assertEqual(self.train_model.shape, (100, 500))
        self.assertEqual(self.test_model.shape, (100, 500))


if __name__ == '__main__':

    tf.logging.set_verbosity(tf.logging.DEBUG)
    tl.logging.set_verbosity(tl.logging.DEBUG)

    unittest.main()
