from fastapi import APIRouter

router = APIRouter()

@router.get("/health", response_model=list[str])
def health():
    return [
        "status: healthy",
        "message: Odoo AI Agent is running smoothly.", 
    ]