import numpy as np
import h5py
import pandas as pd
from sklearn.base import BaseEstimator
from sklearn.utils.multiclass import unique_labels
from imblearn.over_sampling import SMOTE


def one_hot(a, depth):
    b = np.zeros((len(a), depth), dtype=int)
    b[np.arange(len(a)), [int(x) for x in a]] = 1
    return b


def standardize(X, mu=None, std=None):
    if mu is None:
        mu = np.mean(X, 0, keepdims=True)
        std = np.mean(X,0, keepdims=True)
    std[std==0] = 1
    X -= mu
    X /= std
    return X, mu, std


class NineLayerEstimator (BaseEstimator):
    def __init__(self, epochs=200, batch_size=64, feat_norm=True, smote=True, n_classes='auto', verbose=False):
        self.feat_mode = 'average'  # average or time
        self.epochs = epochs
        self.batch_size = batch_size
        self.feat_norm = feat_norm
        self.smote = smote
        self.n_classes = n_classes
        self.verbose = verbose
        self.mdl = None
        self._estimator_type = 'classifier'     # required for proper class stratification in cross_val_predict

    def fit (self, train_x, train_y):
        import tensorflow as tf
        if self.n_classes == 'auto':
            self.classes_ = unique_labels(train_y)
        else:
            self.classes_ = [x for x in range(self.n_classes)]
        nclass = len(self.classes_)
        input_dim = len(train_x[0])

        if self.verbose:
            from collections import Counter
            print (f"NineLayerEstimator: training on {len(train_x)} samples with breakdown: {Counter(train_y)}")

        self.mdl = tf.keras.Sequential([tf.keras.layers.Dense(512, input_shape=(input_dim,), activation='relu'),
                                   tf.keras.layers.BatchNormalization(),
                                   tf.keras.layers.Dropout(0.5),
                                   tf.keras.layers.Dense(512, activation='relu'),
                                   tf.keras.layers.BatchNormalization(),
                                   tf.keras.layers.Dropout(0.5),
                                   tf.keras.layers.Dense(512, activation='relu'),
                                   tf.keras.layers.BatchNormalization(),
                                   tf.keras.layers.Dense(nclass, activation='softmax')])
        self.mdl.compile(optimizer='adam', loss='categorical_crossentropy')

        if self.feat_norm:
            train_x, self.tr_m, self.tr_s = standardize(train_x)
            #test_x = standardize(test_x, tr_m, tr_s)[0]
            if self.smote:
                try:
                    sm = SMOTE(random_state=42)
                    smote_x, smote_y = sm.fit_resample(train_x, train_y)
                except:
                    print ("Error applying SMOTE operation, skipping")
                else:
                    train_x, train_y = smote_x, smote_y

        hot_y = one_hot(train_y, nclass)
        self.mdl.fit(train_x, hot_y, epochs=self.epochs, batch_size=self.batch_size, verbose=self.feat_mode=="time")
        return self

    def predict (self, test_x):
        if self.verbose:
            print (f"NineLayerEstimator: predict {len(test_x)} samples")
        if self.feat_norm:
            test_x = standardize(test_x, self.tr_m, self.tr_s)[0]
        pred_tf = self.mdl.predict(test_x)
        pred_y = np.argmax(pred_tf, -1)
        return pred_y

    def predict_proba (self, test_x):
        if self.verbose:
            print (f"NineLayerEstimator: predict_proba {len(test_x)} samples")
        if self.feat_norm:
            test_x = standardize(test_x, self.tr_m, self.tr_s)[0]
        pred_tf = self.mdl.predict(test_x)
        return pred_tf

