from fastapi import Header , HTTPException 
from core.security import verify_supabase_jwt

async def get_current_user(authorization:str = Header(None))->dict:
  if not authorization:
    raise HTTPException(status_code=401,detail="missing authorization header")
  if not authorization.lower().startswith("bearer "):
    raise HTTPException(status_code=401,detail="Invalid Authorization header")
  
  token = authorization.split(" ",1)[1].strip()

  payload = await verify_supabase_jwt(token)

  return {
    "id":payload["sub"],
    "email":payload.get("email"),
    "role":payload.get("role")
  }



