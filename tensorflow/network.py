import tensorflow
from tensorflow import keras
from tensorflow.keras import layers


class model:

    def __init__(self):
        model = keras.Sequential()
        model.add(keras.Input(shape=(13, 13, 3)))  # 7*7 RGB images
        model.add(layers.Conv2D(35, 5, activation="relu", use_bias=True))
        model.add(layers.Dropout(0.1))
        model.add(layers.Conv2D(35, 3, padding="same", activation="relu", use_bias=True))
        model.add(layers.Dropout(0.1))
        model.add(layers.Conv2D(35, 5, activation="relu", use_bias=True))
        model.add(layers.Dropout(0.1))
        model.add(layers.Conv2D(35, 3, padding="same", activation="relu", use_bias=True))

        # Can you guess what the current output shape is at this point? Probably not.
        # Let's just print it:

        # Now that we have 4x4 feature maps, time to apply global max pooling.
        model.add(layers.GlobalMaxPooling2D())

        # Finally, we add a classification layer.
        model.add(layers.Dense(30, activation="relu"))
        model.add(layers.Dense(30, activation="relu"))
        model.add(layers.Dense(2, activation="softmax"))

        model.summary()

        model.compile(
            optimizer=keras.optimizers.RMSprop(learning_rate=1e-3),
            loss=keras.losses.SparseCategoricalCrossentropy(),
            metrics=[keras.metrics.SparseCategoricalAccuracy()],
        )


