# Arb-inter-exchange
Arbitrage inter exchange. 

Both Exchanges are configured in json file.

## Installation
1. Create python environnement. 
```bash
# on windows
python -m venv env
env\scripts\activate
```
2. Clone this repo and install requirement
```bash
git clone 'https://github.com/memsjava/arb-inter-exchange.git'
pip install -r requirements.txt
```
3. Get api keys and deposit to your account

As we use ccxt, so the exchange which work are listed in the link:
https://docs.ccxt.com/en/latest/exchange-markets.html

4. Change settings.json 
```
{
    "API_EXCHANGE_NAME_PRIMARY": "", \\binance, kraken, ftx, bybit... in lowerCase, 
    "API_PUBLIC_PRIMARY": "",
    "API_SECRET_PRIMARY": "",
    "API_EXCHANGE_NAME_SECONDARY": "",
    "API_PUBLIC_SECONDARY": "",
    "API_SECRET_SECONDARY": "",
    "live_trading": false, \\ true or false.
    "interest": 0.5, \\ minimum interest percentage by each arb
    "pair": "BTC/USDT",
    "capital": 20 \\ example 20 usdt in primary exchange and it;s corresponding value in btc in second exchange
}
```
4. run the ap
```
python main.py
```
