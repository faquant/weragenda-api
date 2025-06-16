from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo dos dados recebidos
class DadosFrase(BaseModel):
    horario: str
    bloco: str
    frase: str

# Endpoint principal
@app.post("/enviar-frase")
def enviar_frase(dados: DadosFrase):
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/spreadsheets"
    ]

    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "weragenda_service_account.json", scope)
    client = gspread.authorize(creds)

    spreadsheet_id = "11OcXj1Xkqs3vs66QWAFg8BI_Gir9zlcn4MgeFvjS6Iw"
    sheet = client.open_by_key(spreadsheet_id).worksheet("Alterações")

    data = datetime.now().strftime("%Y-%m-%d %H:%M")
    sheet.append_row([data, dados.horario, "Frase", f"{dados.bloco} → {dados.frase}"])

    return {"message": "Frase registrada com sucesso"}

# ✅ Rota raiz adicionada corretamente
@app.get("/")
def root():
    return {"status": "API WERAGENDA online"}
