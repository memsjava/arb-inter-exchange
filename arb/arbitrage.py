async def compute_diff_percentage(exchange_1, exchange_2, symbol, capital):
    res, err = None, None
    try:
        price_1 = exchange_1.fetchOrderBook(symbol, 1)
        price_1 = price_1['bids'][0][0]
        fee_rate_1 = 1 / 100
        capital_ = capital * (1 - fee_rate_1) / price_1
        res['amount_1'] = capital
        res['amount_2'] = capital_
        price_2 = exchange_2.fetchOrderBook(symbol, 1)
        price_2 = price_2['asks'][0][0]
        fee_rate_2 = 1 / 100
        capital_ = price_2 * capital_ * (1 - fee_rate_2)
        res['percentage'] = (capital_ - capital) / capital * 100
        res['price_1'] = price_1
        res['price_2'] = price_2

    except Exception as e:
        err = e
    return res, err


async def get_percentage(exchange_1, exchange_2, symbol, capital, side):
    res, err = None, None

    if side.upper() == exchange_1.name.upper():
        res, err = await compute_diff_percentage(exchange_1, exchange_2,
                                                 symbol, capital)
    else:
        res, err = await compute_diff_percentage(exchange_2, exchange_1,
                                                 symbol, capital)

    return res, err
