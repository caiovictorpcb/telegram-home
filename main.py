from telethon import TelegramClient, events
from home_broker import make_fenri_trade, get_home_broker_payload_from_fenri_message, update_credentials
from datetime import datetime, timedelta
import threading
import os

API_ID = os.environ.get("TELEGRAM_API_ID")
API_HASH = os.environ.get("TELEGRAM_API_HASH")

client = TelegramClient('session_name', API_ID, API_HASH)


def make_trade(payload: dict):
    trade_id, data = make_fenri_trade(payload)
    if trade_id is not None:
        print(f"Trade criado com ID: {trade_id}")
    else:
        print(f"Erro ao criar trade: {payload['ticker_symbol']}; {payload['direction']}; {payload['start_time_utc']}; {payload['duration_milliseconds']}")
        print(f"error: {data}")


def schedule_function(run_time: str, func, *args, **kwargs):

    now = datetime.now()
    try:
        target_time = datetime.strptime(run_time, "%H:%M").replace(year=now.year, month=now.month, day=now.day) - timedelta(seconds=10)

        delay = (target_time - now).total_seconds()
        threading.Timer(delay, func, args, kwargs).start()
        print(f"Function scheduled to run at: {target_time}")
    except ValueError:
        print("Invalid time format. Please ensure the time is in HH:mm format.")

async def main():
    await client.start()
    print("Conectado ao Telegram!")
    update_credentials()

    chats = [-1002350028496, -1002453860229, -1002385840999, -1001701910837]

    @client.on(events.NewMessage(chats=chats))
    async def handler(event):
        """Callback para novas mensagens."""
        message = event.message.message
        print(f"Nova mensagem em um dos chats: {message}")
        if "Investimento Identificado" in message or "Trade confirmado" in message or "ANÁLISE CONFIRMADA" in message:
            print("Mensagem de investimento identificada!")
            isOtc = "(OTC)" in message or "OTC" in message
            payload, horario_aposta = get_home_broker_payload_from_fenri_message(message, isOtc)
            print(f"{payload['ticker_symbol']}; {payload['direction']}; {payload['start_time_utc']}; {payload['duration_milliseconds']}")
            schedule_function(horario_aposta, make_trade, payload)

    print("Escutando novas mensagens...")
    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())
