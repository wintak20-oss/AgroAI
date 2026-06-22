from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from app.auth.dependencies import get_current_user
from app.services.ai_service import get_ai_service
from app.utils.file_storage import save_image
from app.services.websocket_manager import manager

router = APIRouter()


@router.post("/predict")
async def predict(
    file: UploadFile = File(...),
    user=Depends(get_current_user)
):

    try:
        # 1. Read image
        content = await file.read()

        if not content:
            raise HTTPException(status_code=400, detail="Empty file")

        # 2. Save image
        file_path = save_image(content)

        # 3. AI prediction (DIRECT CALL - NO CELERY)
        ai = get_ai_service()
        result = ai.predict(file_path)

        response = {
            "disease": result["disease"],
            "confidence": float(result["confidence"]),
            "user": user["email"]
        }

        # 4. Real-time WebSocket broadcast (optional)
        await manager.broadcast({
            "event": "new_prediction",
            "data": response
        })

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))