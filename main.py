from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from pathlib import Path
import pandas as pd
import re
import os
from dotenv import load_dotenv
import openai

# Guardar respuestas o crear historial de ellas en un txt
from datetime import datetime
def guardar_pregunta_txt(pregunta):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linea = f"[{now}] {pregunta}\n"
    with open("preguntas.txt", "a", encoding="utf-8") as archivo:
        archivo.write(linea)

# Cargar variables de entorno
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# Activar CORS para permitir acceso desde frontend local
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo de datos para las preguntas
class Pregunta(BaseModel):
    pregunta: str

# Cargar respuestas desde CSV
archivo_csv = Path(__file__).parent / "respuestas_demo.csv"
respuestas_demo = pd.read_csv(archivo_csv)

# Palabras comunes para filtrar
STOPWORDS = {"de", "la", "el", "en", "los", "las", "y", "a", "un", "una", "por", "qué", "cuál", "cuáles", "dónde", "cómo", "para", "es"}

def limpiar_palabras(texto):
    palabras = re.findall(r"\b\w+\b", texto.lower(), re.UNICODE)
    return [p for p in palabras if p not in STOPWORDS]

def buscar_respuesta_simulada(pregunta_usuario):
    tokens_usuario = set(limpiar_palabras(pregunta_usuario))
    mejor_coincidencia = None
    puntaje_mayor = 0

    for _, row in respuestas_demo.iterrows():
        tokens_pregunta = set(limpiar_palabras(row["pregunta"]))
        coincidencias = tokens_usuario.intersection(tokens_pregunta)
        puntaje = len(coincidencias)

        if puntaje > puntaje_mayor:
            puntaje_mayor = puntaje
            mejor_coincidencia = row["respuesta"]

    if puntaje_mayor == 0:
        return "🤖 Lo siento, esa información está fuera de mis conocimientos actuales."
    return mejor_coincidencia

@app.post("/preguntar")
async def preguntar(pregunta: Pregunta):
    guardar_pregunta_txt(pregunta.pregunta)  # ✅ Esta línea guarda la pregunta en preguntas.txt

    if not openai.api_key or openai.api_key.startswith("sk-reemplaza"):
        respuesta = buscar_respuesta_simulada(pregunta.pregunta)
        return {"respuesta": respuesta}

    try:
        respuesta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un asistente virtual de la Municipalidad de Rancagua."},
                {"role": "user", "content": pregunta.pregunta}
            ]
        )
        return {"respuesta": respuesta["choices"][0]["message"]["content"]}
    except Exception as e:
        return {"respuesta": f"⚠️ Error al obtener la respuesta: {str(e)}"}
