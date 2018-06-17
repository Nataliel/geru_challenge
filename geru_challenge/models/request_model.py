from datetime import datetime
from sqlalchemy import Column, Integer, Text, DateTime
from geru_challenge.models.meta import Base


class RequestModel(Base):
    __tablename__ = 'Request'
    id = Column(Integer, primary_key=True)
    link = Column(Text)
    session_key = Column(Text)
    created_date = Column(DateTime)

    def __unicode__(self):
        return '%s %s %s' % (self.page_name, self.session_key, self.created_date)

    def __repr__(self):
        return "<RequestModel(name='%s %s %s')>" % (self.page_name, self.session_key, self.created_date)

    def __init__(self, request, session_key):
        self.dbsession = request.dbsession
        self.session_key = session_key
        self.link = request.path
        self.created_date = datetime.now()


class RequestQueryset(object):
    def __init__(self, request, session_key=None):
        self.dbsession = request.dbsession
        self.session_key = session_key

    def get_requests(self):
        """
        Get all request of db
        :return: list of request
        """
        return self.dbsession.query(RequestModel).all()

    def get_requests_by_session(self, session_key):
        """
        Get all request of db
        :return: list of request
        """
        return self.dbsession.query(RequestModel).filter_by(session_key=session_key).all()