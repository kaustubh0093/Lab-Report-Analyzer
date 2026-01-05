from pydantic import BaseModel, Field
from typing import List, Optional

class LabEntity(BaseModel):
    test_name: str = Field(..., description="Name of the lab test")
    value: str = Field(..., description="Result value of the test")
    unit: Optional[str] = Field(None, description="Unit of measurement")
    reference_range: Optional[str] = Field(None, description="Standard reference range")
    flag: Optional[str] = Field(None, description="High, Low, or Normal flag")

class AnalysisRequest(BaseModel):
    text: str = Field(..., description="Extracted text from the report to analyze")

class AnalysisResponse(BaseModel):
    entities: List[LabEntity]
    summary: str
    explanation: str
    medication_suggestions: List[str] = Field(default_factory=list, description="List of suggested medications or lifestyle changes")
    follow_up_suggestions: List[str]
    disclaimer: str

class HealthCheck(BaseModel):
    status: str
