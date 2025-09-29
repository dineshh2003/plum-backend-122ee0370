from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Header
from typing import Optional, List
from app.models.schemas import (
    TextProcessRequest, ProcessResponse, OCRResult,
    ValidateRequest, ValidateResponse,
    ChainRunRequest, ChainRunResponse, ChainStepOutput
)
from app.services.ocr import run_ocr
from app.services.chaining import run_chain_on_text
from pydantic import ValidationError

router = APIRouter()

def check_api_key(x_api_key: Optional[str]):
    demo_key = "demo-secret-key"
    if x_api_key != demo_key:
        raise HTTPException(status_code=401, detail="Invalid API key")

@router.post('/process/text', response_model=ProcessResponse)
async def process_text(req: TextProcessRequest, x_api_key: Optional[str] = Header(None)):
    check_api_key(x_api_key)
    if len(req.text) > 20000:
        raise HTTPException(status_code=400, detail='Text too long')
    out = await run_chain_on_text(req.text, req.input_id)
    return { 'input_id': req.input_id, 'status':'success', 'ocr': None, 'result': out, 'meta': {'steps':['analysis','transform','validate']} }

@router.post('/process/image', response_model=ProcessResponse)
async def process_image(input_id: str = Form(...), image: UploadFile = File(...), x_api_key: Optional[str] = Header(None)):
    check_api_key(x_api_key)
    if image.content_type not in ('image/png','image/jpeg'):
        raise HTTPException(status_code=400, detail='Unsupported file type')
    contents = await image.read()
    MAX_IMAGE_BYTES = 8 * 1024 * 1024
    if len(contents) > MAX_IMAGE_BYTES:
        raise HTTPException(status_code=400, detail='Image too large')
    text, conf = run_ocr(contents)
    out = await run_chain_on_text(text, input_id)
    return { 'input_id': input_id, 'status':'success', 'ocr': {'text':text,'confidence':conf}, 'result': out, 'meta': {'steps':['ocr','analysis','transform','validate']} }

@router.post('/validate', response_model=ValidateResponse)
async def validate_payload(req: ValidateRequest, x_api_key: Optional[str] = Header(None)):
    check_api_key(x_api_key)
    # Simple placeholder validation logic:
    # - If payload is empty dict -> invalid
    # - If payload has keys -> valid
    errors: List[str] = []
    if not isinstance(req.payload, dict) or len(req.payload) == 0:
        errors.append("payload must be a non-empty object")
    valid = len(errors) == 0
    recommended_fix = None
    if not valid:
        # naive recommended fix: add example field
        recommended_fix = {"example_field": "example_value"}
    return {"valid": valid, "errors": errors, "recommended_fix": recommended_fix}

@router.post('/chain-run', response_model=ChainRunResponse)
async def chain_run(req: ChainRunRequest, x_api_key: Optional[str] = Header(None)):
    check_api_key(x_api_key)
    steps_out = []
    current_input = req.input.copy() if isinstance(req.input, dict) else {"text": str(req.input)}
    final_result = {}
    # very simple runner: only supports the named steps 'analysis','transform','validate'
    for step in req.chain:
        if step == "analysis":
            text = current_input.get("text", "")
            out = await run_chain_on_text(text, current_input.get("input_id","chain-run"))
            # store the analysis part only to keep outputs small
            step_out = {"step": "analysis", "output": out.get("analysis", {})}
            steps_out.append(ChainStepOutput(step="analysis", output=out.get("analysis", {})))
            # feed transformed to next
            current_input["analysis"] = out.get("analysis", {})
            current_input["text"] = text
            final_result.update(out)
        elif step == "transform":
            text = current_input.get("text", "")
            out = await run_chain_on_text(text, current_input.get("input_id","chain-run"))
            steps_out.append(ChainStepOutput(step="transform", output=out.get("transformed", {})))
            current_input["transformed"] = out.get("transformed", {})
            final_result.update(out)
        elif step == "validate":
            # reuse simple validator from above
            payload = current_input.get("payload", current_input)
            errors = []
            if not isinstance(payload, dict) or len(payload) == 0:
                errors.append("payload must be a non-empty object")
            steps_out.append(ChainStepOutput(step="validate", output={"valid": len(errors) == 0, "errors": errors}))
            final_result["validated"] = len(errors) == 0
        else:
            # unknown step -> return error in step output but continue
            steps_out.append(ChainStepOutput(step=step, output={"error": "unknown step"}))
    return {"input": req.input, "steps": steps_out, "final": final_result}
