from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from backend.api.analyze import get_medical_agent

router = APIRouter()

class ChatRequest(BaseModel):
    context: str
    history: List[Dict[str, str]] # [{"role": "user", "content": "..."}]
    message: str

@router.post("/chat", summary="Chat with the medical report context")
async def chat_with_report(request: ChatRequest):
    try:
        agent = get_medical_agent()
        response = agent.chat(request.history, request.message, request.context)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat Error: {str(e)}")
