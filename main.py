from telethon import TelegramClient, events
from home_broker import make_fenri_trade, get_home_broker_payload_from_fenri_message, update_credentials, check_trade_status
from datetime import datetime, timedelta
import threading
import os

API_ID = os.environ.get("TELEGRAM_API_ID")
API_HASH = os.environ.get("TELEGRAM_API_HASH")

client = TelegramClient('session_name', API_ID, API_HASH)

trade_results = {}

MAX_ATTEMPTS = 3

BASE_BET_AMOUNT = 100

def handle_trade_result(trade_id, payload, attempt, bet_amount):
    success = check_trade_status(trade_id)
    if success:
        print(f"Trade {trade_id} foi bem-sucedido! Retornando ao valor inicial.")
        trade_results[trade_id] = "success"
    else:
        print(f"Trade {trade_id} falhou. Tentativa {attempt + 1} de {MAX_ATTEMPTS}.")
        trade_results[trade_id] = "failure"
        if attempt < MAX_ATTEMPTS:
            next_bet_amount = bet_amount * 2
            payload["start_time_utc"] = datetime.utcnow().isoformat() + "Z"
            print(f"Dobrando o valor da aposta para {next_bet_amount} e tentando novamente.")
            make_trade(payload, attempt + 1, next_bet_amount)
        else:
            print(f"Limite de tentativas alcançado para o trade {trade_id}. Encerrando Gale.")



def make_trade(payload: dict, attempt=1, bet_amount=BASE_BET_AMOUNT):
    payload["bet_value_usd_cents"] = bet_amount
    trade_id, data = make_fenri_trade(payload)
    if trade_id is not None:
        print(f"Trade criado com ID: {trade_id}")
        threading.Timer(61, handle_trade_result, args=(trade_id, payload, attempt, bet_amount)).start()
    else:
        print(f"Erro ao criar trade: {payload['ticker_symbol']}; {payload['direction']}; {payload['start_time_utc']}; {payload['duration_milliseconds']}")
        print(f"error: {data}")


def schedule_function(run_time: str, func, *args, **kwargs):

    now = datetime.now()
    try:
        target_time = datetime.strptime(run_time, "%H:%M").replace(year=now.year, month=now.month, day=now.day)

        delay = (target_time - now).total_seconds()
        threading.Timer(delay, func, args, kwargs).start()
        payload = args[0]
        print(f"Trade de {payload['ticker_symbol']} para {payload['direction']} de duração {payload['duration_milliseconds']} agendado para rodar em: {target_time}")
    except ValueError:
        print("Invalid time format. Please ensure the time is in HH:mm format.")

async def main():
    await client.start()
    print("Conectado ao Telegram!")
    update_credentials()

    chats = [-1002350028496, -1002453860229, -1002385840999, -1001701910837, -1001888375197, -1001780905863]

    @client.on(events.NewMessage(chats=chats))
    async def handler(event):
        message = event.message.message
        if "Investimento Identificado" in message or "Trade confirmado" in message or "ANÁLISE CONFIRMADA" in message or "OPORTUNIDADE ENCONTRADA" in message:
            isOtc = "(OTC)" in message or "OTC" in message
            payload, horario_aposta = get_home_broker_payload_from_fenri_message(message, isOtc)
            schedule_function(horario_aposta, make_trade, payload)

    print("Escutando novas mensagens...")
    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())
