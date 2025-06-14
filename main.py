
from fastapi import FastAPI, Request
from pydantic import BaseModel
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = FastAPI()

# Dados do Google Sheets
SPREADSHEET_ID = "11OcXj1Xkqs3vs66QWAFg8BI_Gir9zlcn4MgeFvjS6Iw"
SHEET_NAME = "Alterações"
JSON_CREDENTIALS_PATH = "weragenda_service_account.json"

# Modelo dos dados recebidos
class FrasePayload(BaseModel):
    horario: str
    bloco: str
    frase: str

@app.post("/enviar-frase")
async def enviar_frase(dados: FrasePayload):
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(JSON_CREDENTIALS_PATH, scope)
        client = gspread.authorize(creds)

        sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)

        data = datetime.now().strftime("%Y-%m-%d %H:%M")
        sheet.append_row([data, dados.horario, "Frase", f"{dados.bloco} → {dados.frase}"])

        return {"status": "sucesso", "mensagem": "✅ Frase enviada para Google Sheets."}

    except Exception as e:
        return {"status": "erro", "detalhe": str(e)}
