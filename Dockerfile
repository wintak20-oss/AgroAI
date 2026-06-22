FROM python:3.11-slim

WORKDIR /app

# =========================
# SYSTEM DEPENDENCIES
# =========================
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# =========================
# PYTHON SETTINGS
# =========================
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# =========================
# INSTALL DEPENDENCIES (OPTIMIZED)
# =========================
COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# =========================
# COPY APPLICATION
# =========================
COPY . .

# =========================
# SECURITY (NON-ROOT USER)
# =========================
RUN useradd -m appuser
USER appuser

# =========================
# HEALTH CHECK
# =========================
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
CMD curl --fail http://localhost:8000/ || exit 1

# =========================
# RUN SERVER (PRODUCTION SAFE FOR TFLITE)
# =========================
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]