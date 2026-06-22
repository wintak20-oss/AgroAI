import os
import numpy as np
import tensorflow as tf

from sklearn.utils.class_weight import compute_class_weight
from tensorflow.keras import layers
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

# =====================================================
# CONFIGURATION
# =====================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, "dataset")

IMG_SIZE = 224
BATCH_SIZE = 32

INITIAL_EPOCHS = 10
FINE_TUNE_EPOCHS = 20

# =====================================================
# LOAD DATASET
# =====================================================

train_ds = tf.keras.utils.image_dataset_from_directory(
    DATASET_PATH,
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE
)

val_ds = tf.keras.utils.image_dataset_from_directory(
    DATASET_PATH,
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE
)

class_names = train_ds.class_names
num_classes = len(class_names)

print("\nClasses:")
for i, name in enumerate(class_names):
    print(f"{i}: {name}")

# =====================================================
# CLASS WEIGHTS
# =====================================================

print("\nCalculating class weights...")

labels = np.concatenate([y.numpy() for _, y in train_ds])

weights = compute_class_weight(
    class_weight="balanced",
    classes=np.unique(labels),
    y=labels
)

class_weights = dict(enumerate(weights))

print("Class Weights:")
print(class_weights)

# =====================================================
# DATA PIPELINE
# =====================================================

AUTOTUNE = tf.data.AUTOTUNE

train_ds = (
    train_ds
    .shuffle(1000)
    .prefetch(AUTOTUNE)
)

val_ds = val_ds.prefetch(AUTOTUNE)

# =====================================================
# DATA AUGMENTATION
# =====================================================

data_aug = tf.keras.Sequential([
    layers.RandomFlip("horizontal_and_vertical"),
    layers.RandomRotation(0.15),
    layers.RandomZoom(0.15),
    layers.RandomContrast(0.2),
])

# =====================================================
# BASE MODEL
# =====================================================

base_model = MobileNetV2(
    input_shape=(IMG_SIZE, IMG_SIZE, 3),
    include_top=False,
    weights="imagenet"
)

base_model.trainable = False

# =====================================================
# MODEL ARCHITECTURE
# =====================================================

inputs = tf.keras.Input(shape=(IMG_SIZE, IMG_SIZE, 3))

x = data_aug(inputs)

x = preprocess_input(x)

x = base_model(x, training=False)

x = layers.GlobalAveragePooling2D()(x)

x = layers.Dense(
    512,
    activation="relu"
)(x)

x = layers.BatchNormalization()(x)

x = layers.Dropout(0.5)(x)

outputs = layers.Dense(
    num_classes,
    activation="softmax"
)(x)

model = tf.keras.Model(inputs, outputs)

model.summary()

# =====================================================
# CALLBACKS
# =====================================================

callbacks = [

    tf.keras.callbacks.ModelCheckpoint(
        filepath="best_model.keras",
        monitor="val_accuracy",
        save_best_only=True,
        verbose=1
    ),

    tf.keras.callbacks.EarlyStopping(
        monitor="val_loss",
        patience=5,
        restore_best_weights=True,
        verbose=1
    ),

    tf.keras.callbacks.ReduceLROnPlateau(
        monitor="val_loss",
        factor=0.2,
        patience=2,
        min_lr=1e-6,
        verbose=1
    )
]

# =====================================================
# STAGE 1 - TRAIN CLASSIFIER HEAD
# =====================================================

print("\n================================")
print("STAGE 1: TRAINING CLASSIFIER")
print("================================")

model.compile(
    optimizer=tf.keras.optimizers.Adam(
        learning_rate=1e-3
    ),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

history1 = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=INITIAL_EPOCHS,
    class_weight=class_weights,
    callbacks=callbacks
)

# =====================================================
# STAGE 2 - FINE TUNING
# =====================================================

print("\n================================")
print("STAGE 2: FINE-TUNING")
print("================================")

base_model.trainable = True

fine_tune_at = len(base_model.layers) - 50

for layer in base_model.layers[:fine_tune_at]:
    layer.trainable = False

print(
    f"Fine-tuning last "
    f"{len(base_model.layers)-fine_tune_at} layers"
)

model.compile(
    optimizer=tf.keras.optimizers.Adam(
        learning_rate=1e-5
    ),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

history2 = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=FINE_TUNE_EPOCHS,
    class_weight=class_weights,
    callbacks=callbacks
)

# =====================================================
# EVALUATE
# =====================================================

print("\n================================")
print("FINAL EVALUATION")
print("================================")

loss, acc = model.evaluate(val_ds)

print(f"\nValidation Loss: {loss:.4f}")
print(f"Validation Accuracy: {acc * 100:.2f}%")

# =====================================================
# SAVE FINAL MODEL
# =====================================================

model.save("plant_disease_model.keras")

print("\nSaved:")
print("plant_disease_model.keras")

# =====================================================
# SAVE LABELS
# =====================================================

with open("labels.txt", "w") as f:
    for label in class_names:
        f.write(label + "\n")

print("labels.txt saved")

print("\n✅ Training Completed Successfully!")