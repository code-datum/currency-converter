from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from model import Exchange, logger
import os
from datetime import date

app = Flask(__name__)
app.config.from_object('config')
api = Api(app)
base_url = '/api/v1'


# def abort_if_code_doesnt_exist(code, exchange):
#     latest_currencies = exchange.get_latest_currency(code)
#     if code not in latest_currencies['rates'][code]:
#         abort(404, message="{} doesn't exist".format(code))


class Convert(Resource):
    def get(self, value, from_currency, to_currency):

        logger.info("START  Convert")
        exchange = Exchange()
        # abort_if_code_doesnt_exist(code=from_currency, exchange=exchange)
        converted_val, error = exchange.convert(value, from_currency=from_currency, to_currency=to_currency)
        if error:
            logger.error(f'{error["msg"]}', 'error')
        today = date.today()
        if converted_val:
            data = {
            "query": "/convert/{}/{}/{}".format(value, from_currency, to_currency),
            "converted_value": converted_val,
            "from": from_currency,
            "to": to_currency,
            "date": str(today)
        }
            logger.info("convert data {}".format(data))
        else:
            data = {
                "query": "/convert/{}/{}/{}".format(value, from_currency, to_currency),
                "converted_value": {},
                "from": from_currency,
                "to": to_currency,
                "date": str(today),
                "error": 1
            }
            logger.info("convert data {}".format(data))
        logger.info("END  Convert")
        return data


class Latest(Resource):
    map_currency = ["CZK", "EUR", "PLN", "USD"]

    def get(self, code):
        exchange = Exchange()
        latest_currencies = exchange.get_latest_currency(code)
        logger.info("START Latest: 'code' is %s", code)
        logger.info("Latest currencies {}".format(latest_currencies))
        today = date.today()
        if "rates" in latest_currencies:
            # rates = {key: latest_currencies['rates'][key] for key in latest_currencies['rates'].keys() - self.map_currency}
            data = {
            "rates": latest_currencies['rates'],
            "base": code,
            "date": str(today)
        }
            logger.info("latest data {}".format(data))
        else:
            data = {
                "rates": {},
                "base": code,
                "date": str(today),
                "error": 1
            }
            logger.error("latest data {}".format(data))
        logger.info("END Latest")
        return data


## Actually setup the Api resource routing here
'''
resource: convert, '/convert/value:/from:/to:'
format: 
    {
        "query": "/convert/19999.95/GBP/EUR",
        "value": 19999.95,
        "from": "GBP",
        "to": "EUR"
        "timestamp": xxxx
    }
'''
api.add_resource(Convert, base_url + "/convert/<value>/<from_currency>/<to_currency>")

'''
api.add latest, '/latest/base/code:'
{
    "rates":{
    "CZK": 1.5785,
    "EUR": 1.4785,
    "PLN": 1.6785,
    "USD": 0.2785,
    }
    ,
     "base": "USD",
  "timestamp": xxx
}
'''
api.add_resource(Latest, base_url + "/latest/base/<code>")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 6000))
    app.run(host='0.0.0.0', port=port)
