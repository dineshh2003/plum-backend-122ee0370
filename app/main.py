from fastapi import FastAPI
from app.api.v1 import router as v1_router

app = FastAPI(title='Problems 5-8 Backend Demo')
app.include_router(v1_router, prefix='/v1')
