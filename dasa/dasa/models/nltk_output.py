from datetime import datetime as dt
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import relationship
from .meta import Base
# from .associations import portfolios_associations
from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    DateTime,
    ForeignKey,
)


class NLTKOutput(Base):
    """ Create the nltk table
    """
    __tablename__ = 'nltk_output'
    id = Column(Integer, primary_key=True)
    nltk_result = Column(Text)
    account_id = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    accounts = relationship('Account', back_populates='nltk_output')
    date_created = Column(DateTime, default=dt.now())
    date_updated = Column(DateTime, default=dt.now(), onupdate=dt.now())


    @classmethod
    def new(cls, request, **kwargs):
        """ Create a new nltk analysis
        """
        if request.dbsession is None:
            raise DBAPIError
        analysis = cls(**kwargs)
        request.dbsession.add(analysis)

        return request.dbsession.query(cls).filter(
            cls.name == kwargs['name']).one_or_none()

    @classmethod
    def all(cls, request):
        """List all the results
        """
        if request.dbsession is None:
            raise DBAPIError

        return request.dbsession.query(cls).all()

    @classmethod
    def one(cls, request, pk=None):
        """List one of the results
        """
        if request.dbsession is None:
            raise DBAPIError
        import pdb; pdb.set_trace()
        return request.dbsession.query(cls).get(pk)

    #  TODO: needs to be locked to a users account
    @classmethod
    def destroy(cls, request=None, pk=None):
        """delete a users results
        """
        if request.dbsession is None:
            raise DBAPIError

        return request.dbsession.query(cls).get(pk).delete()

