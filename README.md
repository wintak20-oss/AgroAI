# 🌱 Digital AgroHealth — AI-Powered Crop Disease Detection

**Digital AgroHealth** is an AI-powered mobile application designed to support **farmers, agricultural extension workers, researchers, and agricultural organizations** in the early identification and management of crop diseases.

The application uses **AI-based image classification** to analyze crop leaf images and provide disease predictions through a mobile interface. It is designed with an **offline-first approach** to support users in areas with limited or unreliable internet connectivity.

## 🎯 Project Objective

The project aims to make crop disease identification more accessible by combining:

* 📷 Crop leaf image analysis
* 🤖 Artificial Intelligence / Machine Learning
* 📱 Mobile technology
* 🌐 Online and offline operation
* 🌾 Agricultural disease information
* 📊 Prediction history and analytics
* 🗣️ Multilingual and voice-assisted interaction

The goal is to help users identify potential crop diseases earlier and access relevant agricultural information without depending entirely on continuous internet connectivity.

---

## ✨ Key Features

### 🤖 AI Crop Disease Detection

Users can capture or select a crop leaf image and receive an AI-generated disease prediction.

The application uses a trained **MobileNetV2-based image classification model** converted to **TensorFlow Lite** for mobile inference.

### 📱 Offline-First AI

The application is designed to continue providing core functionality when internet connectivity is unavailable.

```text
                 ┌──────────────────┐
                 │   Mobile App     │
                 │     Flutter      │
                 └────────┬─────────┘
                          │
                 ┌────────▼─────────┐
                 │ Image Processing │
                 └────────┬─────────┘
                          │
                 ┌────────▼─────────┐
                 │ TensorFlow Lite  │
                 │  MobileNetV2     │
                 └────────┬─────────┘
                          │
                 ┌────────▼─────────┐
                 │ Disease Result   │
                 └──────────────────┘
```

### 🌐 Hybrid AI Architecture

When internet connectivity is available, the application can communicate with the backend API.

When connectivity is unavailable, the mobile application can perform local inference and maintain data locally for later synchronization.

```text
                   User
                    │
                    ▼
              Flutter Mobile App
                    │
          ┌─────────┴─────────┐
          │                   │
       Online              Offline
          │                   │
          ▼                   ▼
     FastAPI Backend      TFLite Model
          │                   │
          ▼                   ▼
    PostgreSQL DB        SQLite Local DB
          │                   │
          └─────────┬─────────┘
                    ▼
             History / Sync
```

---

## 🧠 Machine Learning Model

The disease classification component uses **MobileNetV2** as the base architecture with transfer learning.

### Model Configuration

| Component        | Configuration                    |
| ---------------- | -------------------------------- |
| Base Model       | MobileNetV2                      |
| Input Size       | 224 × 224                        |
| Image Channels   | RGB                              |
| Framework        | TensorFlow / Keras               |
| Mobile Format    | TensorFlow Lite                  |
| Classification   | Multi-class                      |
| Mobile Inference | TFLite                           |
| Preprocessing    | Image resizing and normalization |

The model is optimized for mobile deployment to provide practical inference performance on Android devices.

---

## 🌾 Supported Classes

The current model contains **16 classification categories**:

1. Pepper — Bacterial Spot
2. Pepper — Healthy
3. Potato — Early Blight
4. Potato — Late Blight
5. Potato — Healthy
6. Tomato — Bacterial Spot
7. Tomato — Early Blight
8. Tomato — Late Blight
9. Tomato — Leaf Mold
10. Tomato — Septoria Leaf Spot
11. Tomato — Spider Mites
12. Tomato — Target Spot
13. Tomato — Yellow Leaf Curl Virus
14. Tomato — Mosaic Virus
15. Tomato — Healthy
16. Other / Invalid Image

The **Other / Invalid** category helps the application identify images th
