from pyramid.config import Configurator
from pyramid.events import NewRequest
from pyramid.session import SignedCookieSessionFactory
from geru_challenge.component import request_setup

session_factory = SignedCookieSessionFactory('geruchallengesecret')


def main(global_config, **settings):
    """
    This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.set_session_factory(session_factory)
    config.include('pyramid_jinja2')
    config.include('.models')
    config.include('.routes')
    config.scan()

    config.add_subscriber(request_setup, NewRequest)

    return config.make_wsgi_app()
