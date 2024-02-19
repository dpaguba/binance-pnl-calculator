from binance.client import Client
from dotenv import load_dotenv
from datetime import datetime
import os
import requests  

load_dotenv()

api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET")
api_url = os.getenv("API_URL")

client = Client(api_key, api_secret)

def calculate_pnl(start_date, end_date, symbol):
    start_timestamp = int(datetime.strptime(start_date, '%Y-%m-%d').timestamp()) * 1000
    end_timestamp = int(datetime.strptime(end_date, '%Y-%m-%d').timestamp()) * 1000

    historical_trades = client.futures_account_trades(symbol=symbol, startTime=start_timestamp, endTime=end_timestamp)

    daily_pnl = {}
    for trade in historical_trades:
        date = datetime.utcfromtimestamp(trade['time'] / 1000).strftime('%Y-%m-%d')
        daily_pnl[date] = daily_pnl.get(date, {})
        daily_pnl[date][symbol] = daily_pnl[date].get(symbol, 0.0) + float(trade['realizedPnl'])

    return daily_pnl

# Specify your desired date range
start_date = '2024-02-01'
end_date = '2024-02-07'

symbol_list = ['OPUSDT', 'SUIUSDT', 'ARBUSDT', 'APTUSDT', 'IMXUSDT', 'DYDXUSDT', 'GRTUSDT', 'ALTUSDT', 'MINAUSDT', 'SNXUSDT', 'BLURUSDT', 'GALUSDT']

for symbol in symbol_list:
    daily_pnl = calculate_pnl(start_date, end_date, symbol)

    for date, pnl_data in daily_pnl.items():
        total_pnl = round(sum(pnl_data.values()), 2)
        payload = {"pair": symbol, "date": date, "total": total_pnl}

        response = requests.post(api_url, json=payload)

        if response.status_code == 200 or response.status_code == 201:
            print(f'Data successfully sent to the API for {symbol} on {date}.')
        else:
            print(f'Failed to send data for {symbol} on {date}. Status code: {response.status_code}, Response text: {response.text}')
