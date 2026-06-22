import numpy as np
from PIL import Image
from tflite_runtime.interpreter import Interpreter
from pathlib import Path
import threading

BASE_DIR = Path(__file__).resolve().parent.parent.parent
MODEL_PATH = BASE_DIR / "ml_models" / "best_model.tflite"
LABELS_PATH = BASE_DIR / "ml_models" / "labels.txt"


class AIService:

    def __init__(self):
        self.interpreter = Interpreter(model_path=str(MODEL_PATH))
        self.interpreter.allocate_tensors()

        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

        # thread lock (IMPORTANT for SaaS)
        self.lock = threading.Lock()

        # load labels
        if LABELS_PATH.exists():
            with open(LABELS_PATH, "r", encoding="utf-8") as f:
                self.labels = [line.strip() for line in f.readlines()]
        else:
            self.labels = ["Unknown"]

    # =========================
    # IMAGE PREPROCESSING
    # =========================
    def preprocess(self, image: Image.Image):

        image = image.convert("RGB")

        h, w = self.input_details[0]["shape"][1:3]
        image = image.resize((w, h))

        input_type = self.input_details[0]["dtype"]

        arr = np.array(image)

        # normalize only if float model
        if input_type == np.float32:
            arr = arr.astype(np.float32) / 255.0

        return np.expand_dims(arr, axis=0).astype(input_type)

    # =========================
    # PREDICTION
    # =========================
    def predict(self, image: Image.Image):

        input_data = self.preprocess(image)

        # thread-safe inference
        with self.lock:

            self.interpreter.set_tensor(
                self.input_details[0]["index"],
                input_data
            )

            self.interpreter.invoke()

            output = self.interpreter.get_tensor(
                self.output_details[0]["index"]
            )

        output = np.squeeze(output)

        idx = int(np.argmax(output))
        confidence = float(np.max(output))

        disease = self.labels[idx] if confidence > 0.6 else "Unknown"

        return {
            "disease": disease,
            "confidence": round(confidence * 100, 2)
        }


# =========================
# SINGLETON (IMPORTANT)
# =========================
_ai_service = None

def get_ai_service():
    global _ai_service
    if _ai_service is None:
        _ai_service = AIService()
    return _ai_service