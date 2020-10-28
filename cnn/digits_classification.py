"""
Trains a CNN on the MNIST dataset using keras.
"""
#another digits dataset https://github.com/kensanata/numbers
import numpy as np
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau

# Model / data parameters
num_classes = 10
input_shape = (28, 28, 1)
batch_size = 128
epochs = 15


def get_preprocessed_data():
    """Get MNIST images
        #Arguments:
            None
        #Returns:
            One-hot encoded MNIST images with their labels
    """
    # the data, split between train and test sets
    (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

    # Scale images to the [0, 1] range
    x_train = x_train.astype("float32") / 255
    x_test = x_test.astype("float32") / 255
    # Make sure images have shape (28, 28, 1)
    x_train = np.expand_dims(x_train, -1)
    x_test = np.expand_dims(x_test, -1)
    print("x_train shape:", x_train.shape)
    print(x_train.shape[0], "train samples")
    print(x_test.shape[0], "test samples")

    # convert class vectors to binary class matrices
    y_train = keras.utils.to_categorical(y_train, num_classes)
    y_test = keras.utils.to_categorical(y_test, num_classes)

    return (y_train, y_test)

def build_model(print_summary=True) -> keras.Model:
    """
    Builds convolutional neural network for image classification
    #Arguments:
        None
    #Returns:
        keras model
    """
    model = keras.Sequential()
    model.add(layers.Conv2D(32, kernel_size=(3, 3), activation="relu", input_shape=input_shape))
    model.add(layers.MaxPooling2D(pool_size=(2, 2)))
    model.add(layers.Conv2D(64, kernel_size=(3, 3), activation="relu"))
    model.add(layers.MaxPooling2D(pool_size=(2, 2)))
    model.add(layers.Flatten())
    model.add(layers.Dropout(0.5))
    model.add(layers.Dense(num_classes, activation="softmax"))
    if print_summary:
        model.summary()

    return model

def train_model(model: keras.Model) -> None:
    """
    Trains a keras model from scratch (no pretrained weights)
        #Arguments:
            model: keras model
        #Returns:
            Trained model
    """
    model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
    earlyStopping = EarlyStopping(monitor='val_loss', patience=10, verbose=0, mode='min')
    mcp_save = ModelCheckpoint('ckpt/best_model.hdf5', save_best_only=True, monitor='val_loss', mode='min')
    reduce_lr_loss = ReduceLROnPlateau(monitor='val_loss', factor=0.1, patience=7, verbose=1, epsilon=1e-4, mode='min')
    model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, validation_split=0.1, callbacks=[earlyStopping, mcp_save, reduce_lr_loss])
    return model

def evaluate_model(model: keras.Model) -> None:
    """Evaluates keras model's accuracy on test set.
        #Arguments:
            model: a keras model
        #Returns:
            None
    """
    score = model.evaluate(x_test, y_test, verbose=0)
    print("Test loss:", score[0])
    print("Test accuracy:", score[1])
