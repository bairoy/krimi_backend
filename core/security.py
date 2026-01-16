import os 
from jose import jwt 
from fastapi import HTTPException

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")

if not SUPABASE_URL or not SUPABASE_JWT_SECRET:
  raise RuntimeError("SUPABASE_URL or SUPABASE_JWT_SECRET is missing")

ISSUER = f"{SUPABASE_URL}/auth/v1"

AUDIENCE = "authenticated"

ALGORITHMS = ["HS256"]

async def verify_supabase_jwt(token:str)->dict:
  if not isinstance(token,str) or token.count(".") !=2:
    raise HTTPException(status_code=401, detail="Invalid JWT format")
  
  try:
    payload = jwt.decode(
      token,SUPABASE_JWT_SECRET,algorithms=ALGORITHMS,audience=AUDIENCE,issuer=ISSUER
    )
    return payload 
  except Exception as e: 
    print("JWT error: ",e)
    raise HTTPException(status_code=401,detail="Invalid or expired token")
  

  

