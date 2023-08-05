from abc import ABC, abstractmethod
from copy import deepcopy
import numpy as np

class ModelAuxiliary(ABC):
    """
    Auxiliary class for model definition, including pre-post processing
    """

    def __init__(self, *args, **kwargs):
        self.setup(*args, **kwargs)

    def __call__(self, x):
        return self.postprocess(
            self.predict(self.preprocess(x)),
            deepcopy(x)
        )

    ###########################################################################################
    ## OVERRIDE
    ###########################################################################################

    @abstractmethod
    def setup(self, *args, **kwargs):
        raise NotImplementedError("ModelAuxiliary/setup")

    @abstractmethod
    def preprocess(self, x):
        raise NotImplementedError("ModelAuxiliary/preprocess")

    @abstractmethod
    def predict(self, x):
        raise NotImplementedError("ModelAuxiliary/predict")

    @abstractmethod
    def postprocess(self, x, orig):
        raise NotImplementedError("ModelAuxiliary/postprocess")

    @abstractmethod
    def get_model(self):
        raise NotImplementedError("ModelAuxiliary/get_model")


class ClassificationModelAuxiliary(ModelAuxiliary):

    @abstractmethod
    def class_indices(self):
        raise NotImplementedError("ClassificationModelAuxiliary/get_model")

    def class_vector(self, cl):
        vec = np.zeros(len(self.class_indices()))
        vec[self.class_indices()[cl]] = 1
        return vec.astype('uint8')