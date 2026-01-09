from infra.supabase_client import supabase
from datetime import datetime,timezone

def create_chat_session(user_id:str, title:str | None = None):
  result = supabase.table("chat_sessions").insert({

  "user_id":user_id,
  "title":title,
  "last_active":datetime.now(timezone.utc).isoformat(),
  }).execute()
  print(result)

  return result.data[0]

def save_message(conversation_id:str,role:str,content:str):
  supabase.table("chat_messages").insert({
    "session_id":conversation_id,
    "role":role,
    "content":content
  }).execute()

def update_last_active(conversation_id:str):
  supabase.table("chat_sessions").update({
    "last_active":datetime.now(timezone.utc).isoformat()
  }).eq("id",conversation_id).execute()
  

def get_messages_for_conversation(conversation_id:str):
  res = (
    supabase.from_("chat_messages")
    .select("id,role,content,created_at")
    .eq("session_id",conversation_id)
    .order("created_at",desc=False)
    .execute()

  )
  return res.data or []