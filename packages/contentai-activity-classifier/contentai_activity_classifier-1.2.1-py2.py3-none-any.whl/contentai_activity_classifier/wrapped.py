# Utility file for reading and writing keras models which have a thin sklearn wrapper.


import pickle
from pathlib import Path


# Don't import tensorflow here b/c it's large.  Only do so when needed.


def write_model (model, output_path):
    import tensorflow as tf
    output_path = Path(output_path)
    if not output_path.exists():
        output_path.mkdir()
    tf.keras.models.save_model(model.mdl, (output_path / "keras.tf"))
    tmp = model.mdl
    model.mdl = 0           # this won't pickle
    pickle.dump (model, open(output_path / "wrapper.pkl", 'wb'))
    model.mdl = tmp


def read_model (input_path):
    import tensorflow as tf
    input_path = Path(input_path)
    model = pickle.load(open(input_path / "wrapper.pkl", 'rb'))
    model.mdl = tf.keras.models.load_model(input_path / "keras.tf")
    return model



