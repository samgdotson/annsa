from __future__ import absolute_import, division, print_function
import numpy as np
import tensorflow as tf

from sklearn.preprocessing import FunctionTransformer
from sklearn.pipeline import make_pipeline

from annsa.model_classes import (dae_model_features,
                                 DAE)
from annsa.load_dataset import load_dataset

tf.enable_eager_execution()


def construct_dae():
    """
    Constructs a dense autoencoder.

    Returns:
    --------
    model_features : class dae_model_features
        Contains all features of the DAE model

    optimizer :
    An Operation that updates the variables in var_list.
    If global_step was not None, that operation also increments
    global_step. See documentation for tf.train.Optimizer

    model : Class DAE
    """
    scaler = make_pipeline(FunctionTransformer(np.log1p, validate=False))
    model_features = dae_model_features(
        learning_rate=1e-1,
        l1_regularization_scale=1e-1,
        dropout_probability=0.5,
        batch_size=2**5,
        dense_nodes_encoder=[100],
        dense_nodes_decoder=[],
        scaler=scaler,
        activation_function=tf.nn.relu,
        output_size=1024,
        output_function=None)

    optimizer = tf.train.AdamOptimizer(model_features.learning_rate)
    model = DAE(model_features)
    return model_features, optimizer, model


def test_dae_construction():
    """
    Tests construction of the dense autoencoder.
    """
    _, _, _ = construct_dae()
    pass


def test_dae_training():
    """
    Testing the dense neural network class and training function.
    """

    tf.reset_default_graph()
    model_features, optimizer, model = construct_dae()
    train_dataset, test_dataset = load_dataset('ae')
    model_features.scaler.fit(train_dataset[0])

    all_loss_train, all_loss_test = model.fit_batch(
        train_dataset,
        test_dataset,
        optimizer,
        num_epochs=1,
        earlystop_patience=0,
        verbose=1,
        print_errors=0,
        obj_cost=model.mse,
        earlystop_cost_fn=model.mse,
        data_augmentation=model.default_data_augmentation,)
    pass
