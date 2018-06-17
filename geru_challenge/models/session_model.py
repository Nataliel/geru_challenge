import base64
from datetime import datetime
import os

from pyramid.compat import pickle, bytes_
from sqlalchemy import Column, Integer, Text, DateTime

from geru_challenge.models.meta import Base


class SessionModel(Base):
    __tablename__ = 'Session'
    id = Column(Integer, primary_key=True)
    browser_name = Column(Text)
    session_key = Column(Text)
    created_date = Column(DateTime)

    def __unicode__(self):
        return '%s %s %s' % (self.browser_name, self.session_key, self.created_date)

    def __repr__(self):
        return "<SessionModel(name='%s %s %s')>" % (self.browser_name, self.session_key, self.created_date)

    @staticmethod
    def generate_session_key():
        """
        Generate a session key
        :return: session key
        """
        random = os.urandom(24)
        return base64.b64encode(bytes_(random))

    def __init__(self, request):
        self.dbsession = request.dbsession
        self.browser_name = request.user_agent
        self.session_key = self.generate_session_key()
        self.created_date = datetime.now()


class SessionQueryset(object):

    def __init__(self, request):
        self.dbsession = request.dbsession

    def get_sessions(self):
        """
        Get all session of db
        :return: list of session
        """
        return self.dbsession.query(SessionModel).all()

    def get_session(self, session_key):
        """
        Get only one session by session_key of db
        :return: session
        """
        return self.dbsession.query(SessionModel).filter_by(session_key=session_key).all()

