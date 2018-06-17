from pyramid.response import Response
from pyramid.view import view_config
from geru_challenge.component import db_err_msg, parse_query_to_dict
from geru_challenge.models.session_model import SessionQueryset


@view_config(route_name='get_sessions', renderer='json')
def get_sessions(request):
    """
    Get all sessions of db and pass to api as response
    :param request:
    :return: list of sessions
    """
    session_query = SessionQueryset(request).get_sessions()

    if session_query:
        return parse_query_to_dict(session_query, 'sessions')

    return Response(db_err_msg, content_type='text/plain', status=500)


@view_config(route_name='get_session', renderer='json')
def get_session(request):
    """
    Get all sessions of db and pass to api as response
    :param request:
    :return: list of sessions
    """

    session = request.matchdict.get('session_key', '')
    session_query = SessionQueryset(request).get_session(session)

    if session_query:
        return parse_query_to_dict(session_query, 'session')

    return Response(db_err_msg, content_type='text/plain', status=500)