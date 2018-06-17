from sqlalchemy import Column, Integer, Text
from geru_challenge.models.meta import Base


class QuoteModel(Base):
    __tablename__ = 'QuoteModel'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
