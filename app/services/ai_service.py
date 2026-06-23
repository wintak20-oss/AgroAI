import numpy as np
from PIL import Image
from tflite_runtime.interpreter import Interpreter
from pathlib import Path
import threading
import logging

# =========================
# CONFIG PATHS
# =========================
BASE_DIR = Path(__file__).resolve().parent.parent.parent
MODEL_PATH = BASE_DIR / "ml_models" / "best_model.tflite"
LABELS_PATH = BASE_DIR / "ml_models" / "labels.txt"


# =========================
# LOGGING
# =========================
logger = logging.getLogger("AIService")
logger.setLevel(logging.INFO)


class AIService:
    """
    🚀 Enterprise-grade TFLite inference engine
    Thread-safe, production-ready, scalable
    """

    def __init__(self):

        # =========================
        # LOAD MODEL (ONCE ONLY)
        # =========================
        self.interpreter = Interpreter(model_path=str(MODEL_PATH))
        self.interpreter.allocate_tensors()

        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

        # =========================
        # THREAD SAFETY LOCK
        # =========================
        self.lock = threading.Lock()

        # =========================
        # LOAD LABELS SAFELY
        # =========================
        self.labels = self._load_labels()

        # =========================
        # WARMUP (IMPORTANT FOR LATENCY)
        # =========================
        self._warmup()

        logger.info("AI Service initialized successfully")

    # =========================
    # LABEL LOADER
    # =========================
    def _load_labels(self):
        try:
            with open(LABELS_PATH, "r", encoding="utf-8") as f:
                labels = [line.strip() for line in f.readlines()]
                return labels if labels else ["Unknown"]
        except Exception as e:
            logger.warning(f"Label load failed: {e}")
            return ["Unknown"]

    # =========================
    # WARMUP INFERENCE
    # =========================
    def _warmup(self):
        try:
            dummy_shape = self.input_details[0]["shape"]
            dummy = np.zeros(dummy_shape, dtype=self.input_details[0]["dtype"])

            with self.lock:
                self.interpreter.set_tensor(
                    self.input_details[0]["index"],
                    dummy
                )
                self.interpreter.invoke()

            logger.info("AI model warmup complete")

        except Exception as e:
            logger.warning(f"Warmup failed: {e}")

    # =========================
    # PREPROCESS IMAGE
    # =========================
    def preprocess(self, image: Image.Image):

        if image is None:
            raise ValueError("Invalid image input")

        image = image.convert("RGB")

        height, width = self.input_details[0]["shape"][1:3]
        image = image.resize((width, height))

        arr = np.array(image)

        # normalize only if required
        if self.input_details[0]["dtype"] == np.float32:
            arr = arr.astype(np.float32) / 255.0

        return np.expand_dims(arr, axis=0).astype(self.input_details[0]["dtype"])

    # =========================
    # PREDICT (CORE ENGINE)
    # =========================
    def predict(self, image: Image.Image):

        try:
            input_data = self.preprocess(image)

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

            # confidence threshold (production safety)
            if confidence < 0.50:
                disease = "Unknown"
            else:
                disease = self.labels[idx] if idx < len(self.labels) else "Unknown"

            return {
                "success": True,
                "disease": disease,
                "confidence": round(confidence * 100, 2),
                "model": "tflite-enterprise-v1"
            }

        except Exception as e:
            logger.error(f"Inference error: {e}")

            return {
                "success": False,
                "error": "AI inference failed",
                "detail": str(e)
            }


# =========================
# ENTERPRISE SINGLETON
# =========================
class AIEngine:
    _instance = None
    _lock = threading.Lock()

    @classmethod
    def get(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = AIService()
            return cls._instance