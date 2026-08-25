import os

from dotenv import load_dotenv
from groq import Groq

from src.retrieval.query import query_index

load_dotenv()

MODEL = "openai/gpt-oss-20b"

PROMPT_TEMPLATE = """Sos un asistente que responde preguntas sobre la Ley 27.551 de Alquileres (Argentina).
Respondé la pregunta del usuario basándote ÚNICAMENTE en el siguiente contexto extraído de la ley.
Si el contexto no alcanza para responder, decí que no tenés información suficiente.

Contexto:
{contexto}

Pregunta: {pregunta}

Respuesta:"""


def build_prompt(pregunta: str, chunks: list[str]) -> str:
    contexto = "\n\n".join(chunks)
    return PROMPT_TEMPLATE.format(contexto=contexto, pregunta=pregunta)


def generate_answer(pregunta: str, n_results: int = 3) -> dict:
    results = query_index(pregunta, n_results=n_results)
    chunks = results["documents"][0]
    distancias = results["distances"][0]

    prompt = build_prompt(pregunta, chunks)

    client = Groq(api_key=os.environ["GROQ_API_KEY"])
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
    )

    return {
        "respuesta": response.choices[0].message.content,
        "fuentes": [
            {"chunk": chunk, "distancia": distancia}
            for chunk, distancia in zip(chunks, distancias)
        ],
    }


if __name__ == "__main__":
    pregunta = "¿cuánto puede pedir de depósito el dueño del departamento?"
    resultado = generate_answer(pregunta)
    print(resultado["respuesta"])
