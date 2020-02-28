import logging
from urllib.parse import urlencode
import requests

DECIMAL_INDEX = 2
# Enable logging
logging.basicConfig(filename='debug.log', filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


class Exchange:
    currencies_url = 'https://openexchangerates.org/api/currencies.json'
    base_api_url = 'https://api.exchangeratesapi.io'
    currencies_type = 'currencies'
    latest_type = 'latest'
    round_index = 5

    def __init__(self):
        pass

    def convert(self, value, from_currency, to_currency='USD'):
        error = {}
        '''
        convert currency use extend api
        :param value:
        :param from_currency:
        :param to_currency:
        :return decimal:
        '''
        logger.info("Exchange.convert is run")
        content = self.get_latest_currency(from_currency)
        if 'rates' in content:
            to_currency_unit = content['rates'][to_currency]
            converted_money = round(float(value) * to_currency_unit, self.round_index)

            logger.info("converted currency: %s", converted_money)
            logger.info("Exchange.convert is run")
        else:
            logging.error("data isn't got")
            error = {"msg": "Currency isn't get from API"}
            converted_money = None

        return converted_money, error

    def query_to_api(self, type_query, args):
        if type_query == self.latest_type:
            # https://api.exchangeratesapi.io/latest?base=USD
            prefix_url = '/latest?' + urlencode({'base': args['code']})
            logger.info("prefix url%s", self.base_api_url + prefix_url)
            content = requests.get(url=self.base_api_url + prefix_url).json()
            # content = {}

        elif type_query == self.currencies_type:
            content = requests.get(url=self.currencies_url).json()

        logger.info("query_url's result:{}".format(content))
        return content

    def get_currency_title(self, code):
        '''
        Return by code currencies title
        :return: string
        '''
        # https://openexchangerates.org/api/currencies.json
        currencies_title = self.query_to_api('currencies', self.currencies_type)
        if code in currencies_title:
            return currencies_title[code]
        else:
            return None

    def get_latest_currency(self, from_currency):
        return self.query_to_api('latest', {'code': from_currency})

