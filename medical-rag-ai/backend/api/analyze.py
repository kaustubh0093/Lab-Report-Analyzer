from fastapi import APIRouter, HTTPException
from backend.models.schemas import AnalysisRequest, AnalysisResponse
from backend.rag.clinical_chain import ClinicalChain

router = APIRouter()

# Lazy Loading for Medical Agent
_medical_agent = None

def get_medical_agent():
    global _medical_agent
    if _medical_agent:
        return _medical_agent

    print("Initializing Medical Agent...")
    _medical_agent = ClinicalChain()
    return _medical_agent

@router.post("/analyze", response_model=AnalysisResponse, summary="Analyze extracted medical text")
async def analyze_text(request: AnalysisRequest):
    try:
        agent = get_medical_agent()
        # We no longer pass retriever
        result = agent.run_analysis(request.text)
        return result
    except Exception as e:
        # In a real system, log the error properly
        raise HTTPException(status_code=500, detail=f"Analysis Engine Error: {str(e)}")
