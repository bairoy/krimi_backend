from fastapi import APIRouter, Depends 
from models.chat import ChatRequest, ChatResponse 
from core.auth import get_current_user 
from services.chat_service import handle_message 
from infra.chat_repository import get_messages_for_conversation

router = APIRouter()

@router.post("/chat",response_model=ChatResponse)
async def chat(
  req:ChatRequest,
  user:dict=Depends(get_current_user)
):
  print(user)
  reply = await handle_message(
    user_id=user["id"],
    conversation_id=req.conversation_id,
    message=req.message
  )
  return ChatResponse(**reply)

@router.get("/conversations/{conversation_id}/messages")
async def get_conversation_messages(
  conversation_id:str,
  user = Depends(get_current_user),
):
  return get_messages_for_conversation(conversation_id)