import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

# Load and preprocess the MNIST dataset
mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()

x_train = tf.keras.utils.normalize(x_train, axis=1)
x_test = tf.keras.utils.normalize(x_test, axis=1)

# Build the model
model = tf.keras.models.Sequential([
    tf.keras.layers.Flatten(input_shape=(28, 28)),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(10, activation='softmax')
])

# Compile the model
model.compile(optimizer='adam', 
              loss='sparse_categorical_crossentropy', 
              metrics=['accuracy'])

# Train the model
model.fit(x_train, y_train, epochs=3)

# Save the model
model.save('handwritten_model.keras')

# Load and predict on custom handwritten digit images
image_number = 1
while os.path.isfile(f"digits/digit{image_number}.png"):
    try:
        print(f"Processing digits/digit{image_number}.png...")  # Debugging
        img = cv2.imread(f"digits/digit{image_number}.png", cv2.IMREAD_GRAYSCALE)
        
        # Check if the image was read correctly
        if img is None:
            print(f"Error: Unable to read digits/digit{image_number}.png. Check if the file exists and is valid.")
            break

        # Resize the image to 28x28 pixels
        img = cv2.resize(img, (28, 28))

        # Invert and normalize the image
        img = np.invert(img)  # Invert colors for consistency with MNIST
        img = img / 255.0  # Normalize to match the training data
        img = img.reshape(1, 28, 28)  # Ensure shape matches model input
        
        print(f"Image resized and reshaped: {img.shape}")  # Debugging

        # Make prediction
        prediction = model.predict(img, verbose=0)
        print(f"This digit is probably a {np.argmax(prediction)}")
        
        # Display the image
        plt.imshow(img[0], cmap=plt.cm.binary)
        plt.show()
    except Exception as e:
        print(f"Error processing image {image_number}: {e}")
    finally:
        image_number += 1

print("Processing complete.")
