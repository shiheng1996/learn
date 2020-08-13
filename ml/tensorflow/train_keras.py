import os
import gzip

import tensorflow as tf
from tensorflow import keras
from visual.keras.metric_keras_callback import MetricCollector

import numpy as np

from absl import app as absl_app
from absl import flags

print(tf.__version__)

flags.DEFINE_string(name="data_dir", short_name="dd", default="/tmp", help="The location of the input data.")
flags.DEFINE_string(name="model_dir", short_name="md", default="/tmp", help="The location of the model dir.")
flags.DEFINE_float(name="learning_rate", short_name="lr", default=0.005, help="learning rate of the train")
flags.DEFINE_integer(name="batch_size", short_name="bs", default=32, help="batch size of the dataset")
flags.DEFINE_integer(name="epochs", short_name="ep", default=10, help="traversal the dataset how many times")

FLAGS = flags.FLAGS


def load_data(path):
    files = [
        'train-labels-idx1-ubyte.gz', 'train-images-idx3-ubyte.gz',
        't10k-labels-idx1-ubyte.gz', 't10k-images-idx3-ubyte.gz'
    ]

    paths = []
    for fname in files:
        paths.append(os.path.join(path, fname))

    with gzip.open(paths[0], 'rb') as lbpath:
        y_train = np.frombuffer(lbpath.read(), np.uint8, offset=8)

    with gzip.open(paths[1], 'rb') as imgpath:
        x_train = np.frombuffer(imgpath.read(), np.uint8, offset=16).reshape(len(y_train), 28, 28)

    with gzip.open(paths[2], 'rb') as lbpath:
        y_test = np.frombuffer(lbpath.read(), np.uint8, offset=8)

    with gzip.open(paths[3], 'rb') as imgpath:
        x_test = np.frombuffer(imgpath.read(), np.uint8, offset=16).reshape(len(y_test), 28, 28)

    return (x_train, y_train), (x_test, y_test)


def main(args):
    (train_images, train_labels), (test_images, test_labels) = load_data(FLAGS.data_dir)
    train_images = train_images / 255.0
    test_images = test_images / 255.0

    print('len(train_images): %s' % len(train_images))
    print('len(test_images): %s' % len(test_images))

    class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat', 'Sandal', 'Shirt', 'Sneaker', 'Bag',
                   'Ankle boot']

    # model
    model = keras.Sequential([
        keras.layers.Flatten(input_shape=(28, 28)),
        keras.layers.Dense(128, activation=tf.nn.relu),
        keras.layers.Dense(10, activation=tf.nn.softmax)
    ])
    model.compile(optimizer=tf.train.AdamOptimizer(learning_rate=FLAGS.learning_rate),
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    # train
    callbacks = [
        tf.keras.callbacks.ModelCheckpoint(os.path.join(FLAGS.model_dir, "cp.ckpt"), verbose=1),
        tf.keras.callbacks.TensorBoard(log_dir=FLAGS.model_dir),
        MetricCollector(record_progress_enable=True, batch_size=FLAGS.batch_size, epochs=FLAGS.epochs)
    ]
    model.fit(train_images, train_labels, batch_size=FLAGS.batch_size, epochs=FLAGS.epochs, callbacks=callbacks)

    # evaluate
    test_loss, test_acc = model.evaluate(test_images, test_labels)
    print('Test Accuracy: %s, Test Loss: %s' % (test_acc, test_loss))

    # predict - predict the first test image
    predict_label = class_names[np.argmax(model.predict(test_images[:1])[0])]
    true_label = class_names[test_labels[0]]
    print('predict label: %s, and the true label is: %s' % (predict_label, true_label))


if __name__ == "__main__":
    tf.logging.set_verbosity(tf.logging.INFO)
    absl_app.run(main)
