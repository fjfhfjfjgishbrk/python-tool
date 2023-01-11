import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from os import listdir
from os.path import isfile, join
from tensorflow import keras
import tensorflow as tf
import network
import cv2
import numpy as np
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras import callbacks
import random
import time
import math

w = 30
dropout = 0.3

def initModel():
    model = keras.Sequential()
    model.add(keras.Input(shape=(w, w, 3)))  # RGB images
    model.add(layers.Conv2D(30, 3, activation="relu", use_bias=True))
    model.add(layers.Conv2D(30, 3, padding="same", activation="relu", use_bias=True))
    model.add(layers.BatchNormalization())
    model.add(layers.Conv2D(45, 3, activation="relu", use_bias=True))
    model.add(layers.Conv2D(45, 3, padding="same", activation="relu", use_bias=True))
    model.add(layers.BatchNormalization())
    model.add(layers.MaxPool2D(pool_size=(2, 2)))
    model.add(layers.Conv2D(60, 3, activation="relu", use_bias=True))
    model.add(layers.Conv2D(60, 3, padding="same", activation="relu", use_bias=True))
    model.add(layers.BatchNormalization())
    model.add(layers.Conv2D(75, 3, activation="relu", use_bias=True))
    model.add(layers.Conv2D(75, 3, padding="same", activation="relu", use_bias=True))
    model.add(layers.BatchNormalization())
    model.add(layers.MaxPool2D(pool_size=(2, 2)))
    model.add(layers.Conv2D(90, 3, activation="relu", use_bias=True))
    model.add(layers.Conv2D(90, 3, padding="same", activation="relu", use_bias=True))
    model.add(layers.BatchNormalization())

    # Can you guess what the current output shape is at this point? Probably not.
    # Let's just print it:

    # Now that we have 4x4 feature maps, time to apply global max pooling.
    model.add(layers.GlobalMaxPooling2D())

    # Finally, we add a classification layer.
    model.add(layers.Dense(370, activation="relu"))
    model.add(layers.Dropout(dropout))
    model.add(layers.Dense(370, activation="relu"))
    model.add(layers.Dropout(dropout))
    model.add(layers.Dense(370, activation="relu"))
    model.add(layers.Dropout(dropout))
    model.add(layers.Dense(370, activation="relu"))
    model.add(layers.Dropout(dropout))
    model.add(layers.Dense(2, activation="softmax"))

    model.summary()

    model.compile(
        optimizer=keras.optimizers.RMSprop(learning_rate=2e-4, momentum=0.6),
        loss=keras.losses.SparseCategoricalCrossentropy(),
        metrics=[keras.metrics.SparseCategoricalAccuracy()],
    )
    return model


buildings = [f for f in listdir("landSatBigData/build") if isfile(join("landSatBigData/build", f))]
nonBuildings = [f for f in listdir("landSatBigData/no") if isfile(join("landSatBigData/no", f))]

new = True
test_size = 192
test_chance = 0.08

random.shuffle(buildings)
random.shuffle(nonBuildings)

train_input = np.zeros((1, w, w, 3))
train_output = np.zeros((1, 1))
test_input = np.zeros((1, w, w, 3))
test_output = np.zeros((1, 1))

count = 0
buildLen = len(buildings)
nonBuildLen = len(nonBuildings)

box = ["▏", "▎", "▍", "▌", "▋", "▊", "▉", "█"]
totalBox = 30

timeStart = int(time.time() * 1000)
newDataSet = True

for f in buildings:
    count += 1
    if f.endswith("jpg"):
        img = cv2.imread("landSatBigData/build/" + f)
        if random.random() < test_chance:
            test_input = np.concatenate((test_input, np.array([img])))
            test_output = np.concatenate((test_output, np.array([[1]])))
        else:
            if train_input.shape[0] > 500:
                train_input = train_input[1:]
                train_output = train_output[1:]
                train_input = tf.convert_to_tensor(train_input)
                train_output = tf.convert_to_tensor(train_output)
                if newDataSet:
                    train_dataset = tf.data.Dataset.from_tensor_slices((train_input, train_output))
                    newDataSet = False
                else:
                    train_dataset = train_dataset.concatenate(tf.data.Dataset.from_tensor_slices((train_input, train_output)))
                train_input = np.zeros((1, w, w, 3))
                train_output = np.zeros((1, 1))
            train_input = np.concatenate((train_input, np.array([img])))
            train_output = np.concatenate((train_output, np.array([[1]])))
    now = int(time.time() * 1000)
    percent = count / buildLen
    boxDisplay = math.ceil(totalBox * percent)
    boxB = math.floor((totalBox * percent - boxDisplay) * 8)
    text = "█" * (boxDisplay - 1) + box[boxB] + " " * (totalBox - boxDisplay)
    est = ((now - timeStart) / (count / buildLen) - (now - timeStart)) / 1000
    print("\r", "Loading building data |", text, "| [%d / %d] %.2f sec left  ---- Loading file: %s" % (count, buildLen, est, f), end="", sep="")


print("\r", "Finished loading building data!", sep="")
print("Loaded %d pictures" % count)

count = 0
timeStart = int(time.time() * 1000)

for f in nonBuildings:
    count += 1
    if f.endswith("jpg"):
        img = cv2.imread("landSatBigData/no/" + f)
        if random.random() < test_chance:
            test_input = np.concatenate((test_input, np.array([img])))
            test_output = np.concatenate((test_output, np.array([[0]])))
        else:
            if train_input.shape[0] > 500:
                train_input = train_input[1:]
                train_output = train_output[1:]
                train_input = tf.convert_to_tensor(train_input)
                train_output = tf.convert_to_tensor(train_output)
                if newDataSet:
                    train_dataset = tf.data.Dataset.from_tensor_slices((train_input, train_output))
                    newDataSet = False
                else:
                    train_dataset = train_dataset.concatenate(
                        tf.data.Dataset.from_tensor_slices((train_input, train_output)))
                train_input = np.zeros((1, w, w, 3))
                train_output = np.zeros((1, 1))
            train_input = np.concatenate((train_input, np.array([img])))
            train_output = np.concatenate((train_output, np.array([[0]])))
    now = int(time.time() * 1000)
    percent = count / nonBuildLen
    boxDisplay = math.ceil(totalBox * percent)
    boxB = math.floor((totalBox * percent - boxDisplay) * 8)
    text = "█" * (boxDisplay - 1) + box[boxB] + " " * (totalBox - boxDisplay)
    est = ((now - timeStart) / (count / nonBuildLen) - (now - timeStart)) / 1000
    print("\r", "Loading non-building data |", text, "| [%d / %d] %.2f sec left  ---- Loading file: %s" % (count, nonBuildLen, est, f), end="", sep="")

print("\r", "Finished loading non-building data!", sep="")
print("Loaded %d pictures" % count)

test_input = test_input[1:]
test_output = test_output[1:]

test_input = tf.convert_to_tensor(test_input)
test_output = tf.convert_to_tensor(test_output)
train_input = tf.convert_to_tensor(train_input)
train_output = tf.convert_to_tensor(train_output)


if newDataSet:
    train_dataset = tf.data.Dataset.from_tensor_slices((train_input, train_output))
else:
    train_dataset = train_dataset.concatenate(tf.data.Dataset.from_tensor_slices((train_input, train_output)))
test_dataset = tf.data.Dataset.from_tensor_slices((test_input, test_output))

print("Finished data initialization")

TRAIN_BATCH_SIZE = 32
TEST_BATCH_SIZE = 32
SHUFFLE_BUFFER_SIZE = 10000

train_dataset = train_dataset.shuffle(SHUFFLE_BUFFER_SIZE).batch(TRAIN_BATCH_SIZE)
test_dataset = test_dataset.batch(TEST_BATCH_SIZE)

if new:
    model = initModel()
else:
    model = keras.models.load_model("model-hugeLandSat")
    print("Model loaded")

earlyStopping = callbacks.EarlyStopping(monitor="val_loss",
                                        mode="min", patience=10,
                                        restore_best_weights=True,
                                        verbose=1)

model.fit(train_dataset, epochs=100, validation_data=test_dataset, callbacks=[earlyStopping])
print("Evaluate")
result = model.evaluate(test_dataset)
dict(zip(model.metrics_names, result))
model.save("models/model-hugeLandSat")
