# Created: 2026-01-29 18:30

import base64
import io
import sys
from pathlib import Path

import numpy as np
from flask import Flask, jsonify, render_template, request
from PIL import Image
from tensorflow import keras

app = Flask(__name__)

MODEL_PATH = Path(__file__).parent / "mnist_model.h5"
PARENT_MODEL_PATH = Path(__file__).parent.parent / "desktop_version" / "mnist_model.h5"

model = None


def load_model():
    global model
    if MODEL_PATH.exists():
        model = keras.models.load_model(MODEL_PATH)
    elif PARENT_MODEL_PATH.exists():
        model = keras.models.load_model(PARENT_MODEL_PATH)
    else:
        model = build_and_train_model()
        model.save(MODEL_PATH)


def build_and_train_model():
    m = keras.Sequential([
        keras.layers.Input(shape=(28, 28, 1)),
        keras.layers.Conv2D(32, 3, activation="relu"),
        keras.layers.BatchNormalization(),
        keras.layers.Conv2D(32, 3, activation="relu"),
        keras.layers.BatchNormalization(),
        keras.layers.MaxPooling2D(),
        keras.layers.Dropout(0.25),
        keras.layers.Conv2D(64, 3, activation="relu"),
        keras.layers.BatchNormalization(),
        keras.layers.MaxPooling2D(),
        keras.layers.Dropout(0.25),
        keras.layers.Flatten(),
        keras.layers.Dense(128, activation="relu"),
        keras.layers.BatchNormalization(),
        keras.layers.Dropout(0.5),
        keras.layers.Dense(10, activation="softmax"),
    ])
    m.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])

    (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()
    x_train = (x_train.astype(np.float32) / 255.0)[..., np.newaxis]
    x_test = (x_test.astype(np.float32) / 255.0)[..., np.newaxis]
    m.fit(x_train, y_train, epochs=10, batch_size=128, validation_data=(x_test, y_test), verbose=2)
    return m


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    data = request.json.get("image", "")
    if not data:
        return jsonify({"error": "No image data"}), 400

    # Remove data URL prefix
    if "," in data:
        data = data.split(",")[1]

    # Decode base64 image
    image_bytes = base64.b64decode(data)
    image = Image.open(io.BytesIO(image_bytes)).convert("L")
    image = image.resize((28, 28), Image.Resampling.LANCZOS)

    # Convert to numpy array and normalize
    img_array = np.array(image).astype(np.float32) / 255.0
    img_array = img_array.reshape(1, 28, 28, 1)

    # Predict
    probs = model.predict(img_array, verbose=0)[0]
    prediction = int(np.argmax(probs))
    confidence = float(np.max(probs)) * 100.0

    return jsonify({
        "prediction": prediction,
        "confidence": round(confidence, 1)
    })


if __name__ == "__main__":
    load_model()
    app.run(debug=True, port=5000)
