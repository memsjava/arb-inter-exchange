'''
This is for database management, to handle the state of order.
---------------------------------------------------------------------------
' symbol   Exchange_primary_side | Exchange_primary_name |  | Exchange_primary_in_order
--------------------------------------------------------------------------
'''
from tortoise.models import Model
from tortoise import fields
from tortoise import Tortoise


class Arbdata(Model):
    id = fields.IntField(pk=True)
    symbol = fields.TextField()
    exchange_primary_side_name = fields.TextField()
    exchange_primary_name = fields.TextField()
    exchange_primary_in_order = fields.BooleanField()
    exchange_primary_order_id = fields.IntField()
    exchange_secondary_name = fields.TextField()
    exchange_secondary_in_order = fields.BooleanField()
    exchange_secondary_order_id = fields.IntField()


async def initialize():
    # Here we create a SQLite DB using file "db.sqlite3"
    #  also specify the app name of "models"
    #  which contain models from "app.models"
    await Tortoise.init(db_url='sqlite://db.sqlite3',
                        modules={"models": ["__main__"]})
    # Generate the schema
    await Tortoise.generate_schemas()


async def check_order_not_filled():
    data = Arbdata.filter(id=1)
    if data:
        if data['exchange_primary_in_order'] or data[
                'exchange_secondary_in_order']:
            return True
    return False