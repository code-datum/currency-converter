class Exchange:
    def __init__(self):
        pass

    def test_exchange(value, from_currency, to_currency='USD'):
        logger.info("test_exchange function is run")
        content = get_latest_currency_api(url=BASE_API_URL, code=from_currency)
        from_currency_unit = content['rates'][to_currency]

        if type(value) is str:
            split_value = value.split('$')
            logger.info(split_value)
            if len(split_value) == 2:
                logger.info('{}'.format(float(split_value[0])))
                converted_money = round(float(split_value[0]) * from_currency_unit, DECIMAL_KEY)
            else:
                converted_money = 0
                logger.error('enter incorrect data')
        elif type(value) is float or type(value) is int:
            converted_money = round(value * from_currency_unit, DECIMAL_KEY)
        else:
            logger.error('enter incorrect data')
            converted_money = 0
        logger.info("converted currency: %s", converted_money)
        logger.info("test_exchange function is run")

    def query_to_api(type_query, args):
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
