from fastapi import APIRouter, Depends ,Header
from models.chat import ChatRequest, ChatResponse 
from core.auth import get_current_user 
from services.chat_service import handle_message 
from infra.chat_repository import get_messages_for_conversation
from infra.supabase_client import get_user_supabase_client

router = APIRouter()

@router.post("/chat",response_model=ChatResponse)
async def chat(
  req:ChatRequest,
  user:dict=Depends(get_current_user),
  authorization:str = Header(...)
):
  print(user)
  token = authorization.split(" ",1)[1]
  reply = await handle_message(
    supabase_token=token,
    
    conversation_id=req.conversation_id,
    message=req.message
  )
  return ChatResponse(**reply)

@router.get("/conversations/{conversation_id}/messages")
async def get_conversation_messages(
  conversation_id:str,
  user = Depends(get_current_user),
  authorization:str=Header(...)
):
  token = authorization.split(" ",1)[1]
  supabase = get_user_supabase_client(token)
  return get_messages_for_conversation(supabase,conversation_id)