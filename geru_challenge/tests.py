import unittest
import transaction

from pyramid import testing
from geru_challenge.models.meta import Base

from geru_challenge.models.quote_model import QuoteModel
from geru_challenge.views.quote_views import home_view, get_quotes, get_quote, get_quote_random


def dummy_request(dbsession):
    return testing.DummyRequest(dbsession=dbsession)


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