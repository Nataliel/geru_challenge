import random
import requests

from pyramid.response import Response
from geru_challenge.component import geru_api, api_err_msg


class QuoteQueryset(object):

    @staticmethod
    def get_quotes():
        """
        Get all quotes of GERU API
        :return: list of quotes
        """
        return requests.get(geru_api + 'quotes')

    @staticmethod
    def get_quote(number):
        """
        Get only one quote of GERU API
        :param number: quote number string
        :return: quote
        """
        return requests.get('%s%s%s' % (geru_api, 'quotes/', number))

    def get_quote_random(self):
        """
        Get a random quote of GERU API
        :return: random quote
        """
        quotes_api = self.get_quotes()
        if quotes_api.status_code == 200:
            quotes_dict = dict(quotes_api.json())
            quote_random = random.randint(0, len(quotes_dict.values()))
            return requests.get('%s%s%s' % (geru_api, 'quotes/', quote_random))

        return Response(api_err_msg, content_type='text/plain', status=500)