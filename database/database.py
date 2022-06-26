'''
This is for database management, to handle the state of order.
---------------------------------------------------------------------------
' symbol   Exchange_primary_side | Exchange_primary_name |  | Exchange_primary_in_order
--------------------------------------------------------------------------
'''
import orm_sqlite


class Arbdata(orm_sqlite.Model):
    id = orm_sqlite.IntegerField(primary_key=True)  # auto-increment
    symbol = orm_sqlite.StringField()
    exchange_primary_side_name = orm_sqlite.StringField()
    exchange_primary_name = orm_sqlite.StringField()
    exchange_primary_in_order = orm_sqlite.StringField()
    exchange_primary_order_id = orm_sqlite.IntegerField()
    exchange_secondary_name = orm_sqlite.StringField()
    exchange_secondary_in_order = orm_sqlite.StringField()
    exchange_secondary_order_id = orm_sqlite.IntegerField()


def initialize(symbol,exchange_primary_side_name,exchange_primary_name, exchange_secondary_name):
    try:
        db = orm_sqlite.Database('database.sqlite')
        Arbdata.objects.backend = db
        data = Arbdata({'symbol': symbol ,
                        'exchange_primary_side_name': exchange_primary_side_name, 
                        'exchange_primary_name'=exchange_primary_name,
                       'exchange_primary_in_order'='false',
                       'exchange_primary_order_id'=0, 
                       'exchange_secondary_name'=exchange_secondary_name,
                       'exchange_secondary_in_order'='false',
                       'exchange_secondary_order_id'=0 })
        data.save()
    except Exception as e:
        print(e)
