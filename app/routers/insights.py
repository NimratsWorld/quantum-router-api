from fastapi import APIRouter, Depends
from pydantic import BaseModel
import re
from app.security import verify_api_key

router = APIRouter(prefix="/insights", tags=["Data Insights"], dependencies=[Depends(verify_api_key)])

class TextRequest(BaseModel):
    text: str

@router.post("/analyze")
def analyze_text(req: TextRequest):
    emails = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', req.text)
    urls = re.findall(r'https?://[^\s]+', req.text)
    return {"word_count": len(req.text.split()), "emails_found": emails, "urls_found": urls}