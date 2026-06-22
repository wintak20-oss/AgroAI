import time
from collections import defaultdict
from fastapi import Request
from fastapi.responses import JSONResponse

# =========================
# SIMPLE IN-MEMORY RATE LIMITER (SaaS V4 SAFE)
# =========================

REQUEST_LIMIT = 60          # max requests
TIME_WINDOW = 60            # per 60 seconds

# { ip: [timestamps] }
request_log = defaultdict(list)


async def rate_limiter(request: Request, call_next):
    """
    Simple IP-based rate limiter (no Redis required).
    Suitable for MVP / small SaaS deployment.
    """

    ip = request.client.host
    now = time.time()

    # keep only recent requests
    request_log[ip] = [
        timestamp for timestamp in request_log[ip]
        if now - timestamp < TIME_WINDOW
    ]

    # check limit
    if len(request_log[ip]) >= REQUEST_LIMIT:
        return JSONResponse(
            status_code=429,
            content={
                "success": False,
                "message": "Too many requests. Please try again later."
            }
        )

    # record request
    request_log[ip].append(now)

    # continue request
    response = await call_next(request)
    return response