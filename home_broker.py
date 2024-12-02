from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import json
import requests
from datetime import datetime, timedelta
import os
load_dotenv()
import re


prompt = """
Você recebe a seguinte mensagem de investimento:

{message}

Extraia as seguintes informações e as insira no formato JSON e retorne apenas os valores:
- Direção da aposta, se for de venda o valor deve ser "down", se for de compra deve ser "up" (nome do campo: direcao)
- Duração da aposta em milissegundos (exemplo: 60000) (nome do campo: duracao_aposta_ms)
- Símbolo do ativo da aposta, se a aposta for direcionada a alguma empresa, preciso do símbolo da ação da empresa (exemplo: A empresa amazon possui o simbolo "AMZN", a empresa Facebook possui o simbolo "META", a empresa Apple possui o simbolo "AAPL", a empresa Google possui o simbolo "GOOG", a empresa Intel possui o simbolo "INTC", a empresa McDonald's possui o simbolo "MC", a empresa Microsoft possui o simbolo "MSFT", a empresa Tesla possui o simbolo "TSLA", a empresa NVIDIA possui o simbolo NVDA) (nome do campo: simbolo_ativo)
- É criptomoeda? (exemplo: True) (nome do campo: is_cripto)
- Horário de início da entrada (exemplo: 16:15) (nome do campo: horario_inicio_aposta)
"""

template = PromptTemplate.from_template(prompt)

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2
)

chain = template | llm

credentials = {
    "token": None,
    "expiration_date": None
}

home_broker_credentials = {
    "username": os.environ.get("HOME_BROKER_EMAIL"),
    "password": os.environ.get("HOME_BROKER_PASSWORD"),
    "role": "hbb"
}

bet_value_usd_cents = 100
account_type = "demo"


def get_token():
    return credentials["token"]


def list_trades():
    res = requests.get("https://trade-api.homebroker.com/op/user/?account_type=demo&page=0&pagesize=30", headers={
        "Authorization": f'Bearer {get_token()}'
    })
    data = res.json()
    return data


def check_trade_status(trade_id):
    trades = list_trades()
    trade = next((x for x in trades if x["id"] == trade_id), None)
    if trade["result"] == "gain":
        return True
    return False



def format_response(response):
    raw_content = response.json()
    json_data = raw_content.strip("```json").strip("```").strip()
    extracted_data = json.loads(json_data)
    result = json.dumps(extracted_data, indent=2)

    result = json.loads(result)

    content_raw = result["content"]

    cleaned_content = content_raw.replace("```json", "").replace("```", "").strip()

    data = json.loads(cleaned_content)
    return data


def get_home_broker_payload_from_fenri_message(telegram_message, isOtc):
    response = chain.invoke({"message": telegram_message})
    raw_payload = format_response(response)
    isCripto = raw_payload["is_cripto"]
    horario_aposta = raw_payload["horario_inicio_aposta"]
    today = datetime.now()
    time_today = datetime.strptime(horario_aposta, "%H:%M").replace(year=today.year, month=today.month, day=today.day)
    utc_time = time_today + timedelta(hours=3)
    iso_format = utc_time.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    ticker_symbol = raw_payload["simbolo_ativo"] + ('-USD' if isCripto else "") + ('-OTC' if isOtc else '')
    ticker_symbol = re.sub(r'(?<=-USD)-USD', '', ticker_symbol, count=1)
    home_broker_payload = {
        "direction": raw_payload["direcao"],
        "bet_value_usd_cents": bet_value_usd_cents,
        "duration_milliseconds": raw_payload["duracao_aposta_ms"],
        "ticker_symbol": ticker_symbol,
        "account_type": account_type,
        "client_start_price": 1,
        "start_time_utc": iso_format
    }
    return home_broker_payload, horario_aposta


def update_credentials():
    res = requests.post("https://account-manager-api.homebroker.com/login", data=json.dumps(home_broker_credentials))
    data = res.json()
    if "accessToken" not in data:
        print("Erro ao atualizar credenciais.")
        print(data)
        return
    credentials["token"] = data["accessToken"]
    credentials["expiration_date"] = datetime.now() + timedelta(seconds=450)
    print("Credenciais atualizadas com sucesso!")


def make_fenri_trade(payload: dict):
    token = get_token()
    if token is None or datetime.now() > credentials["expiration_date"]:
        update_credentials()
    res = requests.post("https://trade-api-edge.homebroker.com/op/",data=json.dumps(payload), headers= {
        "Authorization": f"Bearer {get_token()}"
    })
    data = res.json()
    if "id" in data:
        return data["id"], data
    return None, data
