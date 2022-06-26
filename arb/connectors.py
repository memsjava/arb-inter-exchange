import ccxt


def connect(exchange_name, api_public, api_secret):
    exchange = None
    try:
        exchange_id = exchange_name.lower()
        exchange_class = getattr(ccxt, exchange_id)
        exchange = exchange_class({'apiKey': api_public, 'secret': api_secret})
    except Exception as e:
        err = e
    return exchange, err


def get_sides(exchange_primary, exchange_secondary, symbol, capital):
    exchange_buy_side, err = None, None
    trade = symbol.split('/')[1]
    crypto = symbol.split('/')[0]
    try:
        balances = exchange_primary.fetch_balance()
        balances_2 = exchange_secondary.fetch_balance()

        if float(balances[trade]['free']) > capital:
            price = float(exchange_secondary.fetchOrderBook(symbol, 1))
            price = price['bids'][0][0]
            if float(balances[trade]['free']) / price <= float(
                    balances_2[crypto]['free']):
                exchange_buy_side = exchange_primary.name
        else:
            if float(balances_2[trade]['free']) > capital:
                price = float(exchange_primary.fetchOrderBook(symbol, 1))
                price = price['bids'][0][0]
                if float(balances_2[trade]['free']) / price <= float(
                        balances[crypto]['free']):
                    exchange_buy_side = exchange_primary.name
    except Exception as e:
        err = e
    return exchange_buy_side, err


def check_current_order():
    # after database implementation
    pass


def send_orders(exchange_primary, exchange_secondary, symbol, res,
                exchange_buy_side):
    order_1, order_2 = None, None
    if exchange_primary.name == exchange_buy_side:
        order_1 = exchange_primary.create_order(symbol, "limit", "buy",
                                                res['amount_1'],
                                                res['price_1'])
        order_2 = exchange_secondary.create_order(symbol, "limit", "sell",
                                                  res['amount_2'],
                                                  res['price_2'])
    else:
        order_1 = exchange_secondary.create_order(symbol, "limit", "buy",
                                                  res['amount_1'],
                                                  res['price_1'])
        order_2 = exchange_primary.create_order(symbol, "limit", "sell",
                                                res['amount_2'],
                                                res['price_2'])
    return order_1, order_2