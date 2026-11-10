from fastapi import Header, HTTPException
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
MASTER_API_KEY = "quantum-factory-secret-2026"

def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != MASTER_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid X-API-Key")
    return x_api_key