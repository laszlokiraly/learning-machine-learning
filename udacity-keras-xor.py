import numpy as np
from keras.utils import np_utils
import tensorflow as tf
# Using TensorFlow 1.0.0; use tf.python_io in later versions
tf.python_io.control_flow_ops = tf

# Set random seed
np.random.seed(42)

# Our data
X = np.array([[0,0],[0,1],[1,0],[1,1]]).astype('float32')
y = np.array([[0],[1],[1],[0]]).astype('float32')


# Initial Setup for Keras
from keras.models import Sequential
from keras.layers.core import Dense, Activation

# Building the model
xor = Sequential()
# y = np_utils.to_categorical(y)
# xor.add(Dense(16, input_dim=2))
# xor.add(Activation("sigmoid"))
# xor.add(Dense(16))
# xor.add(Activation("relu"))
# xor.add(Dense(2))
# xor.add(Activation("sigmoid"))
#
# xor.compile(loss="categorical_crossentropy", optimizer="adam", metrics = ['accuracy'])

xor.add(Dense(8, input_dim=X.shape[1]))
xor.add(Activation('tanh'))
xor.add(Dense(1))
xor.add(Activation('sigmoid'))
xor.compile(loss="binary_crossentropy", optimizer="adam", metrics = ["accuracy"])

# Uncomment this line to print the model architecture
xor.summary()

# Fitting the model
history = xor.fit(X, y, epochs=500, verbose=0)

# Scoring the model
score = xor.evaluate(X, y)
print("\nAccuracy: ", score[-1])

# Checking the predictions
print("\nPredictions:")
print(xor.predict_proba(X))
