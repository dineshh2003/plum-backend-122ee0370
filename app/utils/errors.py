from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi import HTTPException

async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})
