from langchain_core.messages import HumanMessage
from langchain_core.messages import AIMessage
import os 
from agent.myagent import agent
from infra.chat_repository import create_chat_session,save_message,update_last_active


async def handle_message(user_id:str,conversation_id:str|None,message:str):
  title=None
  if conversation_id is None:
    from infra.chat_repository import create_chat_session
    title = " ".join(message.split()[:5])
    session = create_chat_session(user_id=user_id,title=title)
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
  save_message(conversation_id,"user",message)
  save_message(conversation_id,"assistant",reply)
  update_last_active(conversation_id)

  return{
    "conversation_id":conversation_id,
    "reply":reply,
    "title":title
  }

  

 