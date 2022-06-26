# check the balance of TRX side Exchange_1 or 2. sell-side . priceFtx
# check the balance of USDT side Exchange_1 or 2. buy_side. price2

from ftx.client import Client
import json
import kraken.clientKraken as krak
from pykrakenapi import KrakenAPI
import krakenex
import time


class grand_arbitrage_():

    def __init__(self):

        f = open("settings.json")
        config = json.load(f)

        self.clientFtx = Client(
            config['API_PUBLIC_FTX'], config['API_SECRET_FTX'])
        self.sideFtx = None

        api = krakenex.API(config['API_PUBLIC_KRAKEN'],
                           config['API_SECRET_KRAKEN'])
        self.clientKraken = KrakenAPI(api, retry=0)
        self.sideKraken = None

        self.capital = float(config['capital'])
        self.pair = config['pair'].replace('/', '')
        self.pair_ftx = config['pair']

    def readyToArb(self):
        # check any order or positions
        ordersFtx = []
        res = True
        try:
            ordersFtx = self.clientFtx.get_open_orders()
            for orderactive in ordersFtx:
                if orderactive['market'] == self.pair_ftx:
                    print("order open on ftx")
                    res = False
                    break
        except Exception as e:
            print("exception check order ftx", e)

        try:
            orderskraken = self.clientKraken.get_open_orders()
            for desc in orderskraken.descr_order:
                if self.pair in desc:
                    print("order open on kraken")
                    res = False
        except Exception as e:
            print("exception check order kraken", e)

        print("can check arb: ", res)

        return res

    def setSide(self):
        try:
            accountsFtx = self.clientFtx.get_balances()
            for accountFtx in accountsFtx:
                if accountFtx['coin'] == 'USD':
                    if accountFtx['free'] > 15:
                        self.sideFtx = 'buy'        # we hold usdt , ready to buy
                        self.sideKraken = 'sell'
                        self.capital = accountFtx['free']
                        break
                if accountFtx['coin'] == 'CHZ':
                    if accountFtx['free'] > 35:
                        self.capital = accountFtx['free']
                        self.sideFtx = 'sell'
                        self.sideKraken = 'buy'
                        break

            # accountsKrak = self.clientKraken.get_account_balance(otp=None)
            # vol = donnee.loc['CHZ'].vol

            # print(accountsFtx)
            # print("ftx side", self.sideFtx)

            # account1 = 8
            # if account1:
            #     self.sideFtx = 'buy'
            #     self.sideKraken = 'sell'
        except Exception as e:
            print(e)

    def getData(self):
        try:
            res = self.clientFtx.get_orderbook(self.pair_ftx, 20)
            # res = {'asks': [[10854.5, 11.856]], 'bids': [[10854.0, 0.4315]]}

            self.orderBookFtx = {"a": float(
                res['asks'][0][0]), "b": float(res['bids'][0][0])}

            res = krak.getOrderbook(self.pair)
            self.orderBookKraken = {"a": float(
                res['asks'][0][0]), "b": float(res['bids'][0][0])}
            # self.orderBookFtx = {"b": 0.07712, "a": 0.07715}
            # self.orderBookKraken = {"b": 0.07730, "a": 0.07740}

            print("kraken", self.orderBookKraken)
            print("ftx", self.orderBookFtx)
        except Exception as e:
            print("getData", e)

    def run(self):
        resOrder = True
        if self.readyToArb():
            self.setSide()
            self.getData()
            capital = self.capital
            trx = 0
            perc = 0
            print(self.sideFtx, self.capital)
            if self.sideFtx == 'buy':
                # buy on ftx and sell on kraken
                priceFtx = self.orderBookFtx['b']
                feesRateFtx = 0.007 / 100
                trx = (capital*(1-feesRateFtx) / priceFtx)

                priceKraken = self.orderBookKraken['a']
                feesRateKraken = 0.2 / 100
                usdt = priceKraken * trx * (1 - feesRateKraken)

                perc = (usdt - capital) / capital * 100

            if self.sideFtx != 'buy':
                # sell on ftx
                priceFtx = self.orderBookFtx['a']
                feesRateFtx = 0.007 / 100
                usdt = priceFtx * capital * (1 - feesRateFtx)

                priceKraken = self.orderBookKraken['b']
                feesRateKraken = 0.2 / 100
                trx = usdt * (1-feesRateKraken) / (priceKraken)

                perc = (trx - capital) / capital * 100

            if perc > 0.05:
                if self.sideFtx == 'buy':
                    print("buy %s @ %s TRX on Ftx and sell @%s TRX on kraken" %
                          (trx, priceFtx, priceKraken))
                    print("capital %s USDT on FTX, last value USDT %s on kraken" %
                          (capital, usdt))

                else:
                    print("sell %s @ %s TRX on ftx and buy @%s TRX on ftx" %
                          (capital, priceKraken, priceFtx))
                    print("capital %s TRX on ftx, last value TRX %s on kraken" %
                          (capital, trx))

                if trx > 0:
                    resOrder = self.sendOrder(capital, trx)

            else:
                print("no opportunity with percentage final", perc, "%")
                resOrder = True
        return resOrder

    def sendOrder(self, capital, trx):
        order1 = None
        order2 = None
        if self.sideFtx == 'buy':
            try:
                order1 = self.clientFtx.create_order(
                    self.pair_ftx, "buy",  self.orderBookFtx['b'], "limit", trx)
            except:
                error = 1
                while error < 3:
                    order1 = self.clientFtx.create_order(
                        self.pair_ftx, "buy",  self.orderBookFtx['b'], "limit", trx)
                    error += 1
                    time.sleep(5)
            try:
                order2 = self.clientKraken.add_standard_order(pair=self.pair, type='sell', ordertype='limit',
                                                              volume=trx, price=self.orderBookKraken['a'], validate=False, trading_agreement='agree')
            except:
                error = 1
                while error < 3:
                    order2 = self.clientKraken.add_standard_order(pair=self.pair, type='sell', ordertype='limit',
                                                                  volume=trx, price=self.orderBookKraken['a'], validate=False, trading_agreement='agree')
                    error += 1
                    time.sleep(5)
        else:
            try:
                order1 = self.clientKraken.add_standard_order(pair=self.pair, type='buy', ordertype='limit', volume=capital,
                                                              price=self.orderBookKraken['b'], validate=False, trading_agreement='agree')
            except:
                error = 1
                while error < 3:
                    order1 = self.clientKraken.add_standard_order(pair=self.pair, type='buy', ordertype='limit', volume=capital,
                                                                  price=self.orderBookKraken['b'], validate=False, trading_agreement='agree')
                    error += 1
                    time.sleep(5)
            try:
                order2 = self.clientFtx.create_order(
                    self.pair_ftx, "sell", self.orderBookFtx['a'], "limit", capital)
            except:
                error = 1
                while error < 3:
                    order2 = self.clientFtx.create_order(
                        self.pair_ftx, "sell", self.orderBookFtx['a'], "limit", capital)
                    error += 1
                    time.sleep(5)

        if order1 and order2:
            return True
        else:
            return False

    def helpToChoose(self):
        res = self.clientFtx.get_spot_markets()
        capital = 50
        pairs = ['MATIC/USD']
        # pairs = ['1INCH/USD', 'AAVE/USD', 'AVAX/USD', 'AXS/USD', 'BAT/USD', 'BCH/USD', 'CRV/USD', 'DAI/USD', 'DAI/USDT', 'DOT/USD', 'DYDX/USD', 'ENJ/USD', 'ETH/USDT', 'GRT/USD', 'LINK/USD', 'LINK/USDT',
        #          'LRC/USD', 'LTC/USDT', 'MANA/USD', 'MATIC/USD', 'OMG/USD', 'RAY/USD', 'REN/USD', 'SAND/USD', 'SHIB/USD', 'SOL/USD', 'SRM/USD', 'SUSHI/USD', 'TRX/USD', 'UNI/USD', 'WBTC/USD', 'XRP/USDT', 'YFI/USD']
        for res_ in res:
            pair = res_['name'].replace('/', '')
            if res_['name'] in pairs:
                order_krak = krak.getOrderbook(pair)
                order_krak = {"a": float(
                    order_krak['asks'][0][0]), "b": float(order_krak['bids'][0][0])}
                priceFtx = float(res_['ask'])
                feesRateFtx = 0.007 / 100
                trx = (capital*(1-feesRateFtx) / priceFtx)

                priceKraken = order_krak['b']
                feesRateKraken = 0.2 / 100
                usdt = priceKraken * trx * (1 - feesRateKraken)

                perc = (usdt - capital) / capital * 100
                if perc > 0:

                    print("buy %s @ %s TRX on Ftx and sell @%s TRX on kraken" %
                          (trx, priceFtx, priceKraken))
                    print("capital %s USDT on FTX, last value USDT %s on kraken" %
                          (capital, usdt))
                else:
                    print("no opportunity with percentage final",
                          perc, "%", "pair: ", pair)

        return pairs

    def main(self):
        start_ = True
        while start_:
            try:
                start_ = self.run()
            except:
                pass
            time.sleep(15)

    def buyftx(self):
        self.getData()
        accountsFtx = self.clientFtx.get_balances()
        for accountFtx in accountsFtx:
            if accountFtx['coin'] == 'USD':
                trx = accountFtx['free']
                break
        order = self.clientFtx.create_order(
            self.pair_ftx, "buy",  self.orderBookFtx['b'], "limit", trx/self.orderBookFtx['b'])
        print(trx, self.orderBookFtx['b'], trx/self.orderBookFtx['b'])
        print(order)


g_a = grand_arbitrage_()
g_a.main()
