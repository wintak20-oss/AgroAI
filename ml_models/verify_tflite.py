import tensorflow as tf

MODEL_PATH = "plant_disease_model.tflite"

print("Loading TFLite model...")

interpreter = tf.lite.Interpreter(model_path=MODEL_PATH)

interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

print("\n===== INPUT DETAILS =====")
for item in input_details:
    print(item)

print("\n===== OUTPUT DETAILS =====")
for item in output_details:
    print(item)

print("\n✅ TFLite model loaded successfully!")