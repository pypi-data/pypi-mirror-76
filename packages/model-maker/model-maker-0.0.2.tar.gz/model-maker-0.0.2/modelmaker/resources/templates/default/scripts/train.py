import os
import numpy as np
from tensorflow import keras
from {{ package_name }}.models import SimpleClassification
from {{ package_name }}.utils import generate_square, generate_circle

######################################################################
# train SimpleClassification
######################################################################

simple_model = SimpleClassification(mode='training')

class ShapesClassDatagen(keras.utils.Sequence):

    def __init__(self, total, batch_size):
        self.total = total
        self.batch_size = batch_size

    def __len__(self):
        return self.total // self.batch_size

    def __getitem__(self, idx):
        
        img_size = (160, 160)

        def _generate_random_shape(img_size):
            rand = np.random.random()
            if rand > 0.66:
                im = generate_circle(img_size)
                cl = simple_model.class_vector("circle")
            elif rand > 0.33:
                im = generate_square(img_size)
                cl = simple_model.class_vector("square")
            else:
                im = np.zeros(img_size)
                cl = simple_model.class_vector("other")

            # apply model preprocessing
            im = simple_model.preprocess(im)

            return im, cl

        batch = [ _generate_random_shape(img_size) for _ in range(self.batch_size) ]
        xs, ys = zip(*batch)

        return np.asarray(xs), np.asarray(ys)

# training parameters
batch_size = 32
epochs = 5

# generate training data
train_data = ShapesClassDatagen(400, batch_size)
val_data = ShapesClassDatagen(400, batch_size)

# train model
keras.backend.clear_session()
model = simple_model.get_model()
model.compile(
    optimizer=keras.optimizers.Adam(),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)
model.fit(train_data, steps_per_epoch=len(train_data), epochs=epochs)

# save model
model_folder = os.path.join(
    os.path.dirname(
        os.path.dirname(
            os.path.realpath(__file__)
        )
    ),
    "models"
)
model.save(os.path.join(model_folder, 'simple_model'))