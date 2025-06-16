from fastapi import FastAPI, Request
import requests

app = FastAPI()

WEBHOOK_URL = "https://weragenda-n8n.onrender.com/webhook/salvar-frase"

@app.post("/enviar-frase")
async def enviar_frase(request: Request):
    data = await request.json()
    print("📨 Dados recebidos na API:", data)

    response = requests.post(WEBHOOK_URL, json=data)
    print("📡 Resposta do N8N:", response.status_code, response.text)

    return {
        "status": "enviado",
        "dados_recebidos": data,
        "n8n_response": response.text
    }

@app.get("/")
def root():
    return {"status": "API WERAGENDA online (webhook: salvar-frase)"}
