from pyramid.response import Response
from pyramid.view import view_config
from geru_challenge.component import api_err_msg
from geru_challenge.models.quote_model import QuoteQueryset


@view_config(route_name='get_quotes', renderer='../templates/quote_list.jinja2')
def get_quotes(request):
    """
    Get all quotes of GERU API and pass as response
    :param request:
    :return: list of quotes
    """
    quote_api = QuoteQueryset().get_quotes()

    if quote_api.status_code == 200:
        return {'quotes_dict': quote_api.json()}

    return Response(api_err_msg, content_type='text/plain', status=500)


@view_config(route_name='get_quote', renderer='../templates/quote.jinja2')
def get_quote(request):
    """
    Get all quotes of GERU API and pass as response
    :param request:
    :return: quote dict
    """
    quote_number = request.matchdict.get('quote_number')
    quote_api = QuoteQueryset().get_quote(quote_number)

    if quote_api.status_code == 200:
        return {'quote_dict': quote_api.json()}

    return Response(api_err_msg, content_type='text/plain', status=500)


@view_config(route_name='get_quote_random', renderer='../templates/quote.jinja2')
def get_quote_random(request):
    """
    Get all quotes of GERU API and pass as response
    :param request:
    :return: quote dict
    """
    quote_api = QuoteQueryset().get_quote_random()

    if quote_api.status_code == 200:
        return {'quote_dict': quote_api.json()}

    return Response(api_err_msg, content_type='text/plain', status=500)
