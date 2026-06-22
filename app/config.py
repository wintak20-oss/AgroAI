import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # =========================
    # APP CONFIG
    # =========================
    APP_NAME = "Agro AI SaaS"
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"

    # =========================
    # SECURITY
    # =========================
    SECRET_KEY = os.getenv("SECRET_KEY", "change-this-secret")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)
    )

    # =========================
    # DATABASE
    # =========================
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql://agro:agro123@db:5432/agrodb"
    )

    # =========================
    # UPLOADS
    # =========================
    UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")

    # =========================
    # AI MODEL
    # =========================
    MODEL_PATH = os.getenv("MODEL_PATH", "ml_models/best_model.tflite")
    LABELS_PATH = os.getenv("LABELS_PATH", "ml_models/labels.txt")


settings = Settings()