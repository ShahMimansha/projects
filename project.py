import random
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Activation, Input
from tensorflow.keras.optimizers import RMSprop

# Load the dataset
filepath = tf.keras.utils.get_file(
    'shakespeare.txt', 'https://storage.googleapis.com/download.tensorflow.org/data/shakespeare.txt'
)
text = open(filepath, 'rb').read().decode(encoding='utf-8').lower()

# Use a subset of the text
text = text[300000:800000]

# Create character mappings
characters = sorted(set(text))
char_to_index = {c: i for i, c in enumerate(characters)}
index_to_char = {i: c for i, c in enumerate(characters)}

# Define sequence length and step size
SEQ_LENGTH = 40
STEP_SIZE = 3

# Prepare input and output sequences
sentences = []
next_characters = []
for i in range(0, len(text) - SEQ_LENGTH, STEP_SIZE):
    sentences.append(text[i: i + SEQ_LENGTH])
    next_characters.append(text[i + SEQ_LENGTH])

# One-hot encode the input and output
x = np.zeros((len(sentences), SEQ_LENGTH, len(characters)), dtype=np.bool_)
y = np.zeros((len(sentences), len(characters)), dtype=np.bool_)

for i, sentence in enumerate(sentences):
    for t, character in enumerate(sentence):
        x[i, t, char_to_index[character]] = 1
    y[i, char_to_index[next_characters[i]]] = 1

# Build the model
model = Sequential([
    Input(shape=(SEQ_LENGTH, len(characters))),
    LSTM(128),
    Dense(len(characters)),
    Activation('softmax')
])

# Compile the model
model.compile(loss='categorical_crossentropy', optimizer=RMSprop(learning_rate=0.01))

# Train the model
model.fit(x, y, batch_size=256, epochs=4)

# Save the model in the recommended format
model.save('text_generator.keras')  # Recommended format for saving

# Function to sample the next character
def sample(preds, temperature=1.0):
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds + 1e-8) / temperature  # Avoid log(0)
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)

# Function to generate text
def generate_text(length, temperature):
    start_index = random.randint(0, len(text) - SEQ_LENGTH - 1)
    generated = ''
    sentence = text[start_index: start_index + SEQ_LENGTH]
    generated += sentence

    for i in range(length):
        x_pred = np.zeros((1, SEQ_LENGTH, len(characters)))
        for t, character in enumerate(sentence):
            x_pred[0, t, char_to_index[character]] = 1

        predictions = model.predict(x_pred, verbose=0)[0]
        next_index = sample(predictions, temperature)
        next_character = index_to_char[next_index]

        generated += next_character
        sentence = sentence[1:] + next_character

    return generated

# Generate text with different temperatures
print("Temperature: 0.2")
print(generate_text(300, 0.2))
print("\n------0.4------")
print(generate_text(300, 0.4))
print("\n------0.6------")
print(generate_text(300, 0.6))
print("\n------0.8------")
print(generate_text(300, 0.8))
print("\n------1.0------")
print(generate_text(300, 1.0))
