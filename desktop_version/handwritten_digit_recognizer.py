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


MODEL_PATH = Path(__file__).parent / "mnist_model.h5"


def build_model() -> keras.Model:
    model = keras.Sequential(
        [
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
    model.fit(x_train, y_train, epochs=10, batch_size=128, validation_data=(x_test, y_test), verbose=2)
    model.save(MODEL_PATH)
    return ModelBundle(model=model)


class RoundedButton(tk.Canvas):
    def __init__(
        self,
        parent,
        text: str,
        command,
        width: int = 120,
        height: int = 45,
        radius: int = 22,
        bg_color: str = "#000000",
        fg_color: str = "#ffffff",
        hover_color: str = "#333333",
    ) -> None:
        super().__init__(parent, width=width, height=height, bg=parent["bg"], highlightthickness=0)
        self.command = command
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.hover_color = hover_color
        self.radius = radius
        self.btn_width = width
        self.btn_height = height

        self._draw_button(self.bg_color)
        self.text_id = self.create_text(
            width // 2,
            height // 2,
            text=text,
            fill=self.fg_color,
            font=("Helvetica", 13, "bold"),
        )

        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_click)

    def _draw_button(self, color: str) -> None:
        self.delete("btn")
        r = self.radius
        w, h = self.btn_width, self.btn_height
        self.create_arc(0, 0, r * 2, r * 2, start=90, extent=90, fill=color, outline=color, tags="btn")
        self.create_arc(w - r * 2, 0, w, r * 2, start=0, extent=90, fill=color, outline=color, tags="btn")
        self.create_arc(0, h - r * 2, r * 2, h, start=180, extent=90, fill=color, outline=color, tags="btn")
        self.create_arc(w - r * 2, h - r * 2, w, h, start=270, extent=90, fill=color, outline=color, tags="btn")
        self.create_rectangle(r, 0, w - r, h, fill=color, outline=color, tags="btn")
        self.create_rectangle(0, r, w, h - r, fill=color, outline=color, tags="btn")
        self.tag_lower("btn")

    def _on_enter(self, event) -> None:
        self._draw_button(self.hover_color)
        self.config(cursor="hand2")

    def _on_leave(self, event) -> None:
        self._draw_button(self.bg_color)

    def _on_click(self, event) -> None:
        if self.command:
            self.command()


class DigitCanvas:
    # Color palette
    BG_COLOR = "#1a1a2e"
    CARD_COLOR = "#16213e"
    CANVAS_BG = "#0f0f1a"
    ACCENT_COLOR = "#e94560"
    ACCENT_HOVER = "#ff6b6b"
    TEXT_COLOR = "#eaeaea"
    TEXT_SECONDARY = "#a0a0a0"
    SUCCESS_COLOR = "#4ecca3"
    BRUSH_COLOR = "#e94560"
    BUTTON_BG = "#000000"
    BUTTON_HOVER = "#333333"

    def __init__(self, root: tk.Tk, model: ModelBundle) -> None:
        self.root = root
        self.model = model
        self.canvas_size = 392
        self.grid_size = 28
        self.cell_size = self.canvas_size // self.grid_size
        self.grid = np.zeros((self.grid_size, self.grid_size), dtype=np.float32)
        self._bg_image: Optional[tk.PhotoImage] = None
        self._predicted = False

        self.root.title("Digit Recognizer")
        self.root.configure(bg=self.BG_COLOR)
        self.root.resizable(False, False)

        # Main container
        main_frame = tk.Frame(root, bg=self.BG_COLOR)
        main_frame.pack(padx=30, pady=30)

        # Title
        title_label = tk.Label(
            main_frame,
            text="Handwritten Digit Recognizer",
            font=("Helvetica", 24, "bold"),
            bg=self.BG_COLOR,
            fg=self.TEXT_COLOR,
        )
        title_label.pack(pady=(0, 5))

        subtitle_label = tk.Label(
            main_frame,
            text="Draw a number from 0-9",
            font=("Helvetica", 12),
            bg=self.BG_COLOR,
            fg=self.TEXT_SECONDARY,
        )
        subtitle_label.pack(pady=(0, 20))

        # Canvas container with border effect
        canvas_frame = tk.Frame(
            main_frame,
            bg=self.ACCENT_COLOR,
            padx=3,
            pady=3,
        )
        canvas_frame.pack()

        self.canvas = tk.Canvas(
            canvas_frame,
            width=self.canvas_size,
            height=self.canvas_size,
            bg=self.CANVAS_BG,
            highlightthickness=0,
            bd=0,
        )
        self.canvas.pack()
        self._draw_canvas_background()

        # Result label
        self.predict_label = tk.Label(
            main_frame,
            text="Draw a digit and press Predict",
            font=("Helvetica", 16),
            bg=self.BG_COLOR,
            fg=self.TEXT_SECONDARY,
            pady=15,
        )
        self.predict_label.pack(pady=(20, 10))

        # Button container
        button_frame = tk.Frame(main_frame, bg=self.BG_COLOR)
        button_frame.pack(pady=(10, 0))

        # Rounded buttons
        self.predict_button = RoundedButton(
            button_frame,
            text="Predict",
            command=self.predict,
            bg_color=self.BUTTON_BG,
            fg_color=self.TEXT_COLOR,
            hover_color=self.BUTTON_HOVER,
        )
        self.predict_button.pack(side=tk.LEFT, padx=8)

        self.clear_button = RoundedButton(
            button_frame,
            text="Clear",
            command=self.clear,
            bg_color=self.BUTTON_BG,
            fg_color=self.TEXT_COLOR,
            hover_color=self.BUTTON_HOVER,
        )
        self.clear_button.pack(side=tk.LEFT, padx=8)

        self.quit_button = RoundedButton(
            button_frame,
            text="Quit",
            command=self.root.destroy,
            bg_color=self.BUTTON_BG,
            fg_color=self.TEXT_COLOR,
            hover_color=self.BUTTON_HOVER,
        )
        self.quit_button.pack(side=tk.LEFT, padx=8)

        self.canvas.bind("<B1-Motion>", self.on_draw)
        self.canvas.bind("<Button-1>", self.on_draw)

    def _draw_canvas_background(self) -> None:
        self.canvas.delete("bg")
        self._bg_image = tk.PhotoImage(width=self.canvas_size, height=self.canvas_size)
        self._bg_image.put(self.CANVAS_BG, to=(0, 0, self.canvas_size, self.canvas_size))
        self.canvas.create_image(0, 0, image=self._bg_image, anchor="nw", tags=("bg",))
        self.canvas.tag_lower("bg")

    def on_draw(self, event: tk.Event) -> None:
        if self._predicted:
            self.clear()
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
                    self.canvas.create_rectangle(
                        x0, y0, x1, y1,
                        fill=self.BRUSH_COLOR,
                        outline=self.BRUSH_COLOR,
                    )

    def predict(self) -> None:
        image = self.grid.astype(np.float32)[..., np.newaxis]
        image = image.reshape(1, 28, 28, 1)
        probs = self.model.model.predict(image, verbose=0)[0]
        prediction = int(np.argmax(probs))
        confidence = float(np.max(probs)) * 100.0
        self.predict_label.config(
            text=f"Prediction: {prediction}  |  Confidence: {confidence:.1f}%",
            fg=self.SUCCESS_COLOR,
        )
        self._predicted = True

    def clear(self) -> None:
        self.grid.fill(0.0)
        self.canvas.delete("all")
        self._draw_canvas_background()
        self.predict_label.config(
            text="Draw a digit and press Predict",
            fg=self.TEXT_SECONDARY,
        )
        self._predicted = False


def main() -> int:
    model = load_or_train_model()
    root = tk.Tk()
    DigitCanvas(root, model)
    root.mainloop()
    return 0


if __name__ == "__main__":
    sys.exit(main())
