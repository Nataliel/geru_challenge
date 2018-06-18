import unittest
import transaction

from pyramid import testing
from geru_challenge.component import parse_query_to_dict
from geru_challenge.models import SessionModel, RequestModel
from geru_challenge.models.meta import Base

from geru_challenge.models.quote_model import QuoteModel
from geru_challenge.models.request_model import RequestQueryset
from geru_challenge.models.session_model import SessionQueryset
from geru_challenge.views.quote_views import home_view, get_quotes, get_quote, get_quote_random
from geru_challenge.views.request_views import get_requests, get_requests_by_session
from geru_challenge.views.session_views import get_sessions, get_session


def dummy_request(dbsession, user_agent=None):
    return testing.DummyRequest(dbsession=dbsession, user_agent=user_agent)


class BaseTest(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp(settings={
            'sqlalchemy.url': 'sqlite:///:memory:'
        })
        self.config.include('.models')
        settings = self.config.get_settings()

        from .models import (
            get_engine,
            get_session_factory,
            get_tm_session,
            )

        self.engine = get_engine(settings)
        session_factory = get_session_factory(self.engine)

        self.session = get_tm_session(session_factory, transaction.manager)

    def init_database(self):
        Base.metadata.create_all(self.engine)

    def tearDown(self):

        testing.tearDown()
        transaction.abort()
        Base.metadata.drop_all(self.engine)


class TestHomeViewSuccessCondition(BaseTest):
    def setUp(self):
        super(TestHomeViewSuccessCondition, self).setUp()
        self.init_database()

        quote = QuoteModel(name='quote 2.')
        self.session.add(quote)

    def test_passing_view(self):
        info = home_view(dummy_request(self.session))
        self.assertEqual(info['quote'].name, 'quote 2.')
        self.assertEqual(info['project'], 'Web Challenge 1.0')


class TestHomeViewFailureCondition(BaseTest):
    def test_failing_view(self):
        info = home_view(dummy_request(self.session))
        self.assertEqual(info.status_int, 500)


class TestGetQuotesViewSuccessCondition(BaseTest):
    def setUp(self):
        super(TestGetQuotesViewSuccessCondition, self).setUp()
        self.init_database()

        quote_1 = QuoteModel(name='quote 1.')
        self.session.add(quote_1)

        quote_2 = QuoteModel(name='quote 2.')
        self.session.add(quote_2)

    def test_passing_view(self):
        info = get_quotes(dummy_request(self.session))
        response = {'quotes': [{'name': 'quote 1.'}, {'name': 'quote 2.'}]}
        self.assertEqual(info, response)


class TestGetQuotesViewFailureCondition(BaseTest):
    def setUp(self):
        super(TestGetQuotesViewFailureCondition, self).setUp()
        self.init_database()

    def test_failing_view(self):
        info = get_quotes(dummy_request(self.session))
        self.assertEqual(info.status_int, 500)


class TestGetQuoteViewSuccessCondition(BaseTest):
    def setUp(self):
        super(TestGetQuoteViewSuccessCondition, self).setUp()
        self.init_database()

        quote_1 = QuoteModel(id=9, name='quote 9.')
        self.session.add(quote_1)

    def test_passing_view(self):
        request = dummy_request(self.session)
        request.matchdict = {'quote_number': 9}
        info = get_quote(request)
        response = {"quote": 'quote 9.'}
        self.assertEqual(info, response)


class TestGetQuoteViewFailureCondition(BaseTest):
    def setUp(self):
        super(TestGetQuoteViewFailureCondition, self).setUp()
        self.init_database()

        quote_1 = QuoteModel(name='quote 9.')
        self.session.add(quote_1)

    def test_passing_view(self):
        info = get_quote(dummy_request(self.session))
        self.assertEqual(info.status_int, 500)


class TestGetQuoteRandomViewFailureCondition(BaseTest):
    def setUp(self):
        super(TestGetQuoteRandomViewFailureCondition, self).setUp()
        self.init_database()

    def test_passing_view(self):
        info = get_quote_random(dummy_request(self.session))
        self.assertEqual(info.status_int, 500)


class TestGetSessionsViewSuccessCondition(BaseTest):
    def setUp(self):
        super(TestGetSessionsViewSuccessCondition, self).setUp()
        self.init_database()
        session = SessionModel(dummy_request(self.session, 'Firefox'))
        self.session.add(session)

    def test_passing_view(self):
        request = dummy_request(self.session)
        info = get_sessions(request)
        self.assertEqual(info['sessions'][0]['browser_name'], 'Firefox')


class TestGetSessionsViewFailureCondition(BaseTest):
    def setUp(self):
        super(TestGetSessionsViewFailureCondition, self).setUp()
        self.init_database()

    def test_passing_view(self):
        info = get_sessions(dummy_request(self.session))
        self.assertEqual(info.status_int, 500)


class TestGetSessionViewSuccessCondition(BaseTest):
    def setUp(self):
        super(TestGetSessionViewSuccessCondition, self).setUp()
        self.init_database()
        session = SessionModel(dummy_request(self.session, 'Firefox'))
        self.session.add(session)

    def test_passing_view(self):
        request = dummy_request(self.session)
        session_query = SessionQueryset(request).get_sessions()
        session_dict = parse_query_to_dict(session_query, 'session')
        request.matchdict['session_key'] = session_dict['session'][0]['session_key']
        info = get_session(request)
        self.assertEqual(info['session'][0]['browser_name'], 'Firefox')


class TestGetSessionViewFailureCondition(BaseTest):
    def setUp(self):
        super(TestGetSessionViewFailureCondition, self).setUp()
        self.init_database()

    def test_passing_view(self):
        info = get_sessions(dummy_request(self.session))
        self.assertEqual(info.status_int, 500)


class TestGetRequestsViewSuccessCondition(BaseTest):
    def setUp(self):
        super(TestGetRequestsViewSuccessCondition, self).setUp()
        self.init_database()
        session = SessionModel(dummy_request(self.session, 'Safari'))
        self.session.add(session)

        request_1 = RequestModel(dummy_request(self.session, 'Safari'), session.session_key)
        self.session.add(request_1)

    def test_passing_view(self):
        request = dummy_request(self.session)
        request_list = RequestQueryset(request).get_requests()
        request_list_dict = parse_query_to_dict(request_list, 'requests')
        info = get_requests(request)
        self.assertEqual(info['requests'][0]['session_key'], request_list_dict['requests'][0]['session_key'])


class TestGetRequestViewFailureCondition(BaseTest):
    def setUp(self):
        super(TestGetRequestViewFailureCondition, self).setUp()
        self.init_database()

    def test_passing_view(self):
        info = get_requests(dummy_request(self.session))
        self.assertEqual(info.status_int, 500)


class TestGetRequestViewSuccessCondition(BaseTest):
    def setUp(self):
        super(TestGetRequestViewSuccessCondition, self).setUp()
        self.init_database()
        session = SessionModel(dummy_request(self.session, 'Safari'))
        self.session.add(session)

        request_1 = RequestModel(dummy_request(self.session, 'Safari'), session.session_key)
        self.session.add(request_1)

    def test_passing_view(self):
        request = dummy_request(self.session)
        session_list = SessionQueryset(request).get_sessions()
        session_dict = parse_query_to_dict(session_list, 'session')
        request.matchdict['session_key'] = session_dict['session'][0]['session_key']
        info = get_requests_by_session(request)
        self.assertEqual(len(info['request']), 1)
        self.assertEqual(info['request'][0]['session_key'], session_dict['session'][0]['session_key'])
