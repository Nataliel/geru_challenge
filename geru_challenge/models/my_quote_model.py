import random
from sqlalchemy import Column, Integer, Text
from geru_challenge.models.meta import Base


class MyQuoteModel(Base):
    __tablename__ = 'MyQuoteModel'
    id = Column(Integer, primary_key=True)
    name = Column(Text)

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return "<MyQuoteModel(name='%s')>" % self.name


class MyQuoteQueryset(object):

    def __init__(self, request):
        self.dbsession = request.dbsession

    def get_quotes(self):
        """
        Get all quotes of db
        :return: list of quotes
        """
        return self.dbsession.query(MyQuoteModel).order_by(MyQuoteModel.id).all()

    def get_quote(self, quote_number):
        """
        Get only one quote by id
        :param quote_number: quote id
        :return: quote
        """
        return self.dbsession.query(MyQuoteModel).filter_by(id=quote_number).first()

    def get_quote_random(self):
        """
        Get a random quote of db
        :return: random quote
        """
        quote_random = random.randint(1, 10)
        return self.get_quote(quote_number=quote_random)