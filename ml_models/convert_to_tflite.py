import tensorflow as tf
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "best_model.keras"
)

OUTPUT_PATH = os.path.join(
    BASE_DIR,
    "plant_disease_model.tflite"
)

print("Loading best model...")
model = tf.keras.models.load_model(MODEL_PATH)

converter = tf.lite.TFLiteConverter.from_keras_model(model)

converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.target_spec.supported_types = [tf.float16]

print("Converting...")
tflite_model = converter.convert()

with open(OUTPUT_PATH, "wb") as f:
    f.write(tflite_model)

print("✅ TFLite model saved:", OUTPUT_PATH)

keras_size = os.path.getsize(MODEL_PATH) / (1024 * 1024)
tflite_size = os.path.getsize(OUTPUT_PATH) / (1024 * 1024)

print(f"Keras Model : {keras_size:.2f} MB")
print(f"TFLite Model: {tflite_size:.2f} MB")