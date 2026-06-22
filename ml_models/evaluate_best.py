import os
import tensorflow as tf

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, "dataset")

IMG_SIZE = 224
BATCH_SIZE = 32

val_ds = tf.keras.utils.image_dataset_from_directory(
    DATASET_PATH,
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE
)

model = tf.keras.models.load_model("best_model.keras")

loss, acc = model.evaluate(val_ds)

print("Validation Accuracy:", acc * 100)
print("Validation Loss:", loss)