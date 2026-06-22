from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.middleware.rate_limiter import rate_limiter

from app.routes import (
    auth,
    otp,
    predict,
    analytics,
    admin,
    history,
    websocket,
    sync
)

# =========================
# APP INIT
# =========================
app = FastAPI(
    title="Agro AI SaaS",
    version="4.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# =========================
# CORS (FLUTTER + WEB)
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # lock later in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# RATE LIMIT MIDDLEWARE
# =========================
@app.middleware("http")
async def rate_limit_middleware(request, call_next):
    return await rate_limiter(request, call_next)

# =========================
# ROUTES
# =========================
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(otp.router, prefix="/api/otp", tags=["OTP"])
app.include_router(predict.router, prefix="/api", tags=["AI Predict"])
app.include_router(analytics.router, prefix="/api", tags=["Analytics"])
app.include_router(admin.router, prefix="/api", tags=["Admin"])
app.include_router(history.router, prefix="/api", tags=["History"])
app.include_router(websocket.router, prefix="/ws", tags=["WebSocket"])
app.include_router(sync.router, prefix="/api", tags=["Sync"])

# =========================
# HEALTH CHECK
# =========================
@app.get("/")
def root():
    return {
        "status": "ok",
        "service": "Agro AI SaaS",
        "version": "4.0.0"
    }