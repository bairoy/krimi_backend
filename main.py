from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI 
from api.chat import router as chat_router 
from agent.myagent import checkpointer_cm

app = FastAPI(title="Krimi Backend")
app.include_router(chat_router,prefix="/api")

@app.get("/health")
def health():
  return {"status":"ok"}
@app.on_event("shutdown")
def shutdown():
  checkpointer_cm.__exit__(None,None,None)