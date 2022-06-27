import asyncio
import json
import websocket
import _thread
import arb.arbitrage as arb
import arb.connectors as exchange
import database.database as data


class grand_arbitrage_():

    def __init__(self):
        f = open("settings.json")
        config = json.load(f)

        self.exchange_primary = exchange.connect(
            config['API_EXCHANGE_NAME_PRIMARY'], config['API_PUBLIC_PRIMARY'],
            config['API_SECRET_PRIMARY'])

        self.exchange_secondary = exchange.connect(
            config['API_EXCHANGE_NAME_SECONDARY'],
            config['API_PUBLIC_SECONDARY'], config['API_SECRET_SECONDARY'])

        self.capital = float(config['capital'])
        self.symbol = config['pair']
        self.is_live = config['live_trading']
        self.interest = config['interest']
        self.exchange_buy_side = self.get_sides(self.exchange_primary,
                                                self.exchange_secondary,
                                                self.symbol, self.capital)

    def get_sides(self, exchange_primary, exchange_secondary, symbol, capital):
        res, err = exchange.get_sides(exchange_primary, exchange_secondary,
                                      symbol, capital)
        return res

    async def run(self):
        await data.initialize()
        if self.exchange_buy_side:
            if self.exchange_primary.name.upper(
            ) == 'KRAKEN' or self.exchange_secondary.name.upper() == 'KRAKEN':
                _thread.start_new_thread(self.ws_thread, ())
            else:
                while True:
                    try:
                        self.check_opportunity()
                        await asyncio.sleep(300)
                    except:
                        pass
        else:
            print(
                "Please check the amount of crypto in your account accourding your settings"
            )

    async def check_opportunity(self):
        # check if any order is still not close
        if not data.check_order_not_filled():
            res, err = arb.get_percentage(self.exchange_primary,
                                          self.exchange_secondary, self.symbol,
                                          self.capital, self.exchange_buy_side)
            if not err:
                if res['percentage'] > self.interest and self.is_live:
                    order1, order2 = exchange.send_orders(
                        self.exchange_primary, self.exchange_secondary,
                        self.symbol, res, self.exchange_buy_side)
                    exchange.fetch_order_update_database(order1, order2)
        else:
            data = data.Arbdata.get(id=1)
            exchange.fetch_order_update_database(
                data['exchange_primary_order_id'],
                data['exchange_secondary_order_id'])

    async def ws_message(self, ws, message):
        await self.check_opportunity()

    def ws_open(self, ws):
        ws.send(
            '{"event":"subscribe", "subscription":{"name":"ticker"}, "pair":['
            + self.symbol + ']}')

    def ws_thread(self, *args):
        ws = websocket.WebSocketApp("wss://ws.kraken.com/",
                                    on_open=self.ws_open,
                                    on_message=self.ws_message)
        ws.run_forever()


if __name__ == "__main__":
    g_a = grand_arbitrage_()
    g_a.run()