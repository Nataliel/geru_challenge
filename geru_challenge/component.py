from pyramid.events import subscriber, NewRequest
from geru_challenge.models.request_model import RequestModel
from geru_challenge.models.session_model import SessionModel

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

@subscriber(NewRequest)
def request_setup(event):
    request = event.request
    if not request.session.get('s3cr3t_K3Y'):
        session = SessionModel(request)
        request.session['s3cr3t_K3Y'] = session.session_key
        request.dbsession.add(session)

    new_request = RequestModel(request, request.session.get('s3cr3t_K3Y'))
    request.dbsession.add(new_request)


def parse_query_to_dict(query, key_name):
    """
    Auxiliary method to format queries
    :param query: query
    :param key_name: key of dict
    :return: dict formatted - example: {"quotes": ["quote 1.", "quote 2."]}
    """
    if query:
        query_to_dict = {key_name: []}
        for obj in query:
            fields_dict = {}
            for field, value in obj.__dict__.iteritems():
                if field != 'id' and field != '_sa_instance_state':
                    fields_dict[field] = str(value)

            query_to_dict[key_name].append(fields_dict)

        return query_to_dict
