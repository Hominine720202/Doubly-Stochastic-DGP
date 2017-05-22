# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 11:01:40 2017

@author: hrs13
"""

jitter_level = GPflow.settings.numerics.jitter_level
import tensorflow as tf

def normal_sample(mean, var, full_cov=False):
    if full_cov is False:
            N, D = tf.shape(mean)
            z = tf.random_normal((S, N, D), dtype=tf.float64)
            return mean[None, :, :] + z * var[None, :, :] ** 0.5

    else:
        assert S==1
        # mean is ND, var is NND
        N = tf.shape(mean)[0]

        mean = tf.transpose(mean, (1, 0))  # DN
        var = tf.transpose(var, (2, 0, 1))  # DNN
        I = jitter_level * tf.eye(N, dtype=tf.float64)[None, :, :]
        chol = tf.cholesky(var + I)  # DNN

        z = tf.random_normal(tf.shape(mean), dtype=tf.float64)  # DN
        f = mean[:, :, None] + tf.matmul(chol, z[:, :, None])  # DN1

        return tf.transpose(f[:, :, 0])  # ND take out last dim only