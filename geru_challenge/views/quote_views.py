from sqlalchemy.exc import DBAPIError

from pyramid.response import Response
from pyramid.view import view_config
from geru_challenge.component import parse_query_to_dict

from geru_challenge.models.quote_model import QuoteModel, QuoteQueryset


db_err_msg = """
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_geru_challenge_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""


@view_config(route_name='home', renderer='../templates/home.jinja2')
def home_view(request):
    """
    This page is to help the developer in the project setup
    :param request:
    :return:
    """
    try:
        query = request.dbsession.query(QuoteModel)
        quote = query.filter(QuoteModel.name == 'quote 2.').first()
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {'quote': quote, 'project': 'Web Challenge 1.0'}


@view_config(route_name='get_quotes', renderer='json')
def get_quotes(request):
    """
    Get all quotes of db and pass to api as response
    :param request:
    :return: list of quotes
    """
    quote_query = QuoteQueryset(request).get_quotes()

    if quote_query:
        return parse_query_to_dict(quote_query, 'quotes')

    return Response(db_err_msg, content_type='text/plain', status=500)


@view_config(route_name='get_quote', renderer='json')
def get_quote(request):
    """
    Get a quote by id of db and pass to api as response
    :param request:
    :return: just an one quote by id
    """
    quote_number = request.matchdict.get('quote_number')
    quote_query = QuoteQueryset(request).get_quote(quote_number)

    if quote_query:
        return {"quote": quote_query.name}

    return Response(db_err_msg, content_type='text/plain', status=500)


@view_config(route_name='get_quote_random', renderer='json')
def get_quote_random(request):
    """
    Get a random quote of db and pass to api as response
    :param request:
    :return: just an one random quote
    """
    quote_query = QuoteQueryset(request).get_quote_random()

    if quote_query:
        return {"quote": quote_query.name}

    return Response(db_err_msg, content_type='text/plain', status=500)
