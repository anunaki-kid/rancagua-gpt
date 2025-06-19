🔧 INSTRUCCIONES RÁPIDAS – RANCAGUA GPT (MVP)

1. Abre el archivo `.env` y reemplaza:
   OPENAI_API_KEY=sk-reemplaza_con_tu_clave
   👉 con tu clave real de OpenAI desde https://platform.openai.com/api-keys

2. Instala las dependencias:
   pip install -r requirements.txt

3. Inicia el servidor:
   python -m uvicorn main:app --reload

4. Abre en tu navegador:
   http://127.0.0.1:8000/docs

5. Prueba el endpoint `/preguntar` ingresando preguntas como:
   {
     "pregunta": "¿Dónde pago las patentes municipales en Rancagua?"
   }

🚫 ¡No compartas tu archivo `.env` con nadie!
