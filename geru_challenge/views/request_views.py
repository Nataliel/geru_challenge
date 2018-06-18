from pyramid.response import Response
from pyramid.view import view_config
from geru_challenge.component import db_err_msg, parse_query_to_dict
from geru_challenge.models.request_model import RequestQueryset


@view_config(route_name='get_requests', renderer='json')
def get_requests(request):
    """
    Get all requests of db and pass to api as response
    :param request: request response
    :return: list of request
    """
    request_query = RequestQueryset(request).get_requests()

    if request_query:
        return parse_query_to_dict(request_query, 'requests')

    return Response(db_err_msg, content_type='text/plain', status=500)


@view_config(route_name='get_requests_by_session', renderer='json')
def get_requests_by_session(request):
    """
    Get all requests by session_key of db and pass to api as response
    :param request: request response
    :return: list of requests by session
    """
    session = request.matchdict.get('session_key', '')
    request_query = RequestQueryset(request, session).get_requests_by_session(session)

    if request_query:
        return parse_query_to_dict(request_query, 'request')

    return Response(db_err_msg, content_type='text/plain', status=500)
