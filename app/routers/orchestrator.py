from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
import httpx
from app.security import verify_api_key

router = APIRouter(prefix="/orchestrator", tags=["Orchestrator"], dependencies=[Depends(verify_api_key)])

class OrchestratorRequest(BaseModel):
    query: str

@router.post("/smart-process")
async def smart_process(req: OrchestratorRequest):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "http://127.0.0.1:8000/api/v1/router/predict",
                json={"query": req.query},
                headers={"X-API-Key": "quantum-factory-secret-2026"},
                timeout=5.0
            )
            response.raise_for_status()
            return {"orchestration_status": "success", "routing_decision": response.json()}
        except Exception as e:
            return {"orchestration_status": "degraded", "message": str(e)}