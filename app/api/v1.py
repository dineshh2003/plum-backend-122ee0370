from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Header
from app.models.schemas import TextProcessRequest, ProcessResponse, OCRResult
from app.services.ocr import run_ocr
from app.services.chaining import run_chain_on_text
from typing import Optional

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
    text, conf = run_ocr(contents)
    out = await run_chain_on_text(text, input_id)
    return { 'input_id': input_id, 'status':'success', 'ocr': {'text':text,'confidence':conf}, 'result': out, 'meta': {'steps':['ocr','analysis','transform','validate']} }
