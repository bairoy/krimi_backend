from langchain_core.messages import HumanMessage
from langchain_core.messages import AIMessage
import os 
from agent.myagent import agent
from infra.chat_repository import save_message,update_last_active,create_chat_session
from infra.supabase_client import get_user_supabase_client


async def handle_message(supabase_token:str,conversation_id:str|None,message:str):
  title=None
  
  supabase = get_user_supabase_client(supabase_token)
  if conversation_id is None:
    
    title = " ".join(message.split()[:5])
    session = create_chat_session(supabase,title=title)
    conversation_id = session["id"]

  result = agent.invoke(
    {"messages":[HumanMessage(content=message)]},
    config={
      "configurable":{
        "thread_id":conversation_id
      }
    }
  )
  reply = result["messages"][-1].content
  save_message(supabase,conversation_id,"user",message)
  save_message(supabase,conversation_id,"assistant",reply)
  update_last_active(supabase,conversation_id)

  return{
    "conversation_id":conversation_id,
    "reply":reply,
    "title":title
  }

  

 