import tensorflow as tf
from tensorflow import keras        
from modelmaker import ClassificationModelAuxiliary
from .utils import normalize, rescale2d

class SimpleClassification(ClassificationModelAuxiliary):

    def setup(self, mode='production', model_path=None):
        self.mode = mode

        if mode == 'development':
            self.model = keras.models.load_model(model_path)
        elif mode == 'production':
            raise Exception('production mode not implemented')
        elif mode == 'training':
            pass
        else:
            raise Exception('invalid mode')

    def class_indices(self):
        return {
            "other": 0,
            "square": 1,
            "circle": 2
        }

    def get_model(self):
        model = keras.Sequential([
            keras.layers.Flatten(),
            keras.layers.Dense(128, activation=tf.nn.relu),
            keras.layers.Dense(128, activation=tf.nn.relu),
            keras.layers.Dense(128, activation=tf.nn.relu),
            keras.layers.Dense(3, activation=tf.nn.softmax),
        ])
        return model

    def preprocess(self, x):
        y = rescale2d(x, (160, 160))
        return normalize(y, 0, 1)

    def predict(self, x):
        if self.mode == "production":
            raise Exception('production mode not implemented')
        elif self.mode == 'development':
            return self.model.predict(x)
        else:
            raise Exception('invalid mode')

    def postprocess(self, x, orig):
        return x