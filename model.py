import logging
from urllib.parse import urlencode
import requests

BASE_API_URL = 'https://api.exchangeratesapi.io'
DECIMAL_KEY = 2
# Enable logging
logging.basicConfig(filename='error.log', filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


class Exchange:

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
        query_general = {
            'code': to_currency
        }
        content = self.query_to_api('general', query_general)
        if 'rates' in content:
            from_currency_unit = content['rates'][to_currency]
            converted_money = round(float(value) * from_currency_unit, DECIMAL_KEY)

            logger.info("converted currency: %s", converted_money)
            logger.info("Exchange.convert is run")
        else:
            logging.error("data isn't got")
            error = {"msg": "Currency isn't get from API"}
            converted_money = None

        return converted_money, error

    def query_to_api(self, type_query, args):
        if type_query == 'general':
            prefix_url = '/latest?' + urlencode({'base': args['code']})
            content = requests.get(url=BASE_API_URL + prefix_url).json()
        elif type_query == 'history':
            prefix_url = '/history?' + urlencode({'start_at': args['start_at'],
                                                  'end_at': args['end_at'],
                                                  'base': args['base'],
                                                  'symbols': args['symbols']
                                                  })
            content = requests.get(url=BASE_API_URL + prefix_url).json()
        logger.info("query_url's result:{}".format(content))
        return content

    def get_currency_title(self, code):
        return code
