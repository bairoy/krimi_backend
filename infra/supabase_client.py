import os 
from supabase import create_client #,Client
from supabase.client import ClientOptions

from dotenv import load_dotenv

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
# SUPABASE_SERVICE_ROLE_KEY=os.getenv("SUPABASE_SERVICE_ROLE_KEY")

# if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
#   raise RuntimeError("Supabase environment varialbes not set")

# supabase: Client = create_client(
#   SUPABASE_URL,
#   SUPABASE_SERVICE_ROLE_KEY
# )

def get_user_supabase_client(token:str):
  return create_client(
    SUPABASE_URL,
    SUPABASE_ANON_KEY,
    options=ClientOptions(
      headers={
        "Authorization":f"Bearer {token}"
      }
    )
  )