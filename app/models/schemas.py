from pydantic import BaseModel
from typing import Optional, Any, Dict, List

class TextProcessRequest(BaseModel):
    input_id: str
    text: str
    lang: Optional[str] = None

class OCRResult(BaseModel):
    text: str
    confidence: Optional[float] = None

class ProcessResponse(BaseModel):
    input_id: str
    status: str
    ocr: Optional[OCRResult] = None
    result: Dict[str, Any]
    meta: Dict[str, Any]

class ValidateRequest(BaseModel):
    schema_name: str
    payload: Dict[str, Any]

class ValidateResponse(BaseModel):
    valid: bool
    errors: List[str]
    recommended_fix: Optional[Dict[str, Any]] = None

class ChainRunRequest(BaseModel):
    chain: List[str]
    input: Dict[str, Any]

class ChainStepOutput(BaseModel):
    step: str
    output: Dict[str, Any]

class ChainRunResponse(BaseModel):
    input: Dict[str, Any]
    steps: List[ChainStepOutput]
    final: Dict[str, Any]
