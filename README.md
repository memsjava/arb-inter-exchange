# arb-inter-exchange
Arbitrage inter exchange. kraken - ftx

## Installation
1. create python environnement. 
```bash
# on windows
py -m venv env
env\scripts\activate
```
2. clone this repo and install requirement
```bash
git clone 'https://github.com/memsjava/arb-inter-exchange.git'
py install -r requirements.txt
```
3. get api keys and change settings.json 
4. python main.py

```bash
can check arb:  True
kraken {'a': 0.2366, 'b': 0.2362}
ftx {'a': 0.236579, 'b': 0.23648}
buy 18.41961535
no opportunity with percentage final -0.15634678450607364 %

can check arb:  True
kraken {'a': 0.2366, 'b': 0.2362}
ftx {'a': 0.236651, 'b': 0.236517}
buy 18.41961535
no opportunity with percentage final -0.17196602189272475 %
```
