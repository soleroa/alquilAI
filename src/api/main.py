from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.generation.generate import generate_answer

app = FastAPI(title="alquilAI RAG API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    pregunta: str


class Fuente(BaseModel):
    chunk: str
    distancia: float


class QueryResponse(BaseModel):
    respuesta: str
    fuentes: list[Fuente]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):
    return generate_answer(request.pregunta)
