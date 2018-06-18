from sqlalchemy.exc import DBAPIError

from pyramid.response import Response
from pyramid.view import view_config

from geru_challenge.component import db_err_msg
from geru_challenge.models.session_model import SessionQueryset


@view_config(route_name='home', renderer='../templates/home.jinja2')
def home_view(request):
    """
    This page is to help the developer in the project setup
    :param request:
    :return:
    """
    try:
        query = SessionQueryset(request).get_sessions()
        print query
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {'quote': query, 'project': 'Web Challenge 1.0'}
