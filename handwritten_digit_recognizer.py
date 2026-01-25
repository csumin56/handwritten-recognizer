import sys
import tkinter as tk
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import numpy as np
from tensorflow import keras


@dataclass
class ModelBundle:
    model: keras.Model


MODEL_PATH = Path("mnist_model.h5")


def build_model() -> keras.Model:
    model = keras.Sequential(
        [
            keras.layers.Input(shape=(28, 28, 1)),
            keras.layers.Conv2D(16, 3, activation="relu"),
            keras.layers.MaxPooling2D(),
            keras.layers.Conv2D(32, 3, activation="relu"),
            keras.layers.MaxPooling2D(),
            keras.layers.Flatten(),
            keras.layers.Dense(64, activation="relu"),
            keras.layers.Dense(10, activation="softmax"),
        ]
    )
    model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    return model


def load_or_train_model() -> ModelBundle:
    if MODEL_PATH.exists():
        model = keras.models.load_model(MODEL_PATH)
        return ModelBundle(model=model)

    (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()
    x_train = (x_train.astype(np.float32) / 255.0)[..., np.newaxis]
    x_test = (x_test.astype(np.float32) / 255.0)[..., np.newaxis]

    model = build_model()
    model.fit(x_train, y_train, epochs=3, batch_size=128, validation_data=(x_test, y_test), verbose=2)
    model.save(MODEL_PATH)
    return ModelBundle(model=model)


class DigitCanvas:
    def __init__(self, root: tk.Tk, model: ModelBundle) -> None:
        self.root = root
        self.model = model
        self.canvas_size = 280
        self.grid_size = 28
        self.cell_size = self.canvas_size // self.grid_size
        self.grid = np.zeros((self.grid_size, self.grid_size), dtype=np.float32)
        self._bg_image: Optional[tk.PhotoImage] = None

        self.root.title("Handwritten Digit Recognizer")
        self.root.configure(bg="#ffffff")
        self._force_light_mode()
        self._apply_light_palette()

        self.canvas = tk.Canvas(
            root,
            width=self.canvas_size,
            height=self.canvas_size,
            bg="#ffffff",
            highlightthickness=2,
            highlightbackground="#000000",
            highlightcolor="#000000",
            bd=0,
        )
        self.canvas.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
        self._draw_canvas_background()

        self.predict_label = tk.Label(
            root,
            text="Draw a digit and press Predict",
            font=("Helvetica", 14),
            bg="#f6f4ef",
            fg="#2b2a28",
        )
        self.predict_label.grid(row=1, column=0, columnspan=3, pady=5)

        self.predict_button = tk.Button(root, text="Predict", command=self.predict)
        self.predict_button.grid(row=2, column=0, padx=5, pady=5)

        self.clear_button = tk.Button(root, text="Clear", command=self.clear)
        self.clear_button.grid(row=2, column=1, padx=5, pady=5)

        self.quit_button = tk.Button(root, text="Quit", command=self.root.destroy)
        self.quit_button.grid(row=2, column=2, padx=5, pady=5)

        self.canvas.bind("<B1-Motion>", self.on_draw)
        self.canvas.bind("<Button-1>", self.on_draw)

    def _force_light_mode(self) -> None:
        try:
            self.root.tk.call("tk", "appearance", "light")
        except tk.TclError:
            pass

    def _apply_light_palette(self) -> None:
        try:
            self.root.tk_setPalette(
                background="#ffffff",
                foreground="#000000",
                activeBackground="#ffffff",
                activeForeground="#000000",
                highlightBackground="#000000",
                highlightColor="#000000",
            )
        except tk.TclError:
            pass

    def _draw_canvas_background(self) -> None:
        self.canvas.delete("bg")
        self._bg_image = tk.PhotoImage(width=self.canvas_size, height=self.canvas_size)
        self._bg_image.put("#ffffff", to=(0, 0, self.canvas_size, self.canvas_size))
        self.canvas.create_image(0, 0, image=self._bg_image, anchor="nw", tags=("bg",))
        self.canvas.tag_lower("bg")

    def on_draw(self, event: tk.Event) -> None:
        x, y = event.x, event.y
        col = x // self.cell_size
        row = y // self.cell_size
        if 0 <= row < self.grid_size and 0 <= col < self.grid_size:
            self.apply_brush(row, col)

    def apply_brush(self, row: int, col: int) -> None:
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                rr = row + dr
                cc = col + dc
                if 0 <= rr < self.grid_size and 0 <= cc < self.grid_size:
                    self.grid[rr, cc] = 1.0
                    x0 = cc * self.cell_size
                    y0 = rr * self.cell_size
                    x1 = x0 + self.cell_size
                    y1 = y0 + self.cell_size
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill="black", outline="black")

    def predict(self) -> None:
        image = self.grid.astype(np.float32)[..., np.newaxis]
        image = image.reshape(1, 28, 28, 1)
        probs = self.model.model.predict(image, verbose=0)[0]
        prediction = int(np.argmax(probs))
        confidence = float(np.max(probs)) * 100.0
        self.predict_label.config(text=f"Predicted digit: {prediction} (confidence: {confidence:.1f}%)")

    def clear(self) -> None:
        self.grid.fill(0.0)
        self.canvas.delete("all")
        self._draw_canvas_background()
        self.predict_label.config(text="Draw a digit and press Predict")


def main() -> int:
    model = load_or_train_model()
    root = tk.Tk()
    DigitCanvas(root, model)
    root.mainloop()
    return 0


if __name__ == "__main__":
    sys.exit(main())
