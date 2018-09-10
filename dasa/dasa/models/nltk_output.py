from datetime import datetime as dt
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import relationship
from .nltk_logic import analyze
from .meta import Base
import json
# from .associations import portfolios_associations
from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    String,
    JSON,
    DateTime,
    ForeignKey,
    cast
)


class NLTKOutput(Base):
    """ Create the nltk table
    """
    __tablename__ = 'nltk_output'
    id = Column(Integer, primary_key=True)
    nltk_result = Column(JSON)
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
        unmodified_obj = analyze(kwargs['text'])
        mod_sent = {}
        for sent in unmodified_obj['Sentences']:
            mod_sent[sent] = unmodified_obj['Sentences'][sent][1]
        mod_obj = {'Sentences': mod_sent, 'Body': unmodified_obj['Body']}
        kwargs['nltk_result'] = json.dumps(mod_obj)
        kwargs.pop('text', None)


        # fake_obj = {"account_id": 1, "nltk_result": json.dumps(['string'])}
        nltk = cls(**kwargs)
        # nltk = cls(**fake_obj)
        request.dbsession.add(nltk)
        # request.dbsession.flush()
        return [request.dbsession.query(cls).filter(
            cast(cls.nltk_result, String) == kwargs['nltk_result']).one_or_none(), 
            unmodified_obj]

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
        return request.dbsession.query(cls).get(pk)

    #  TODO: needs to be locked to a users account
    @classmethod
    def destroy(cls, request=None, pk=None):
        """delete a users results
        """
        if request.dbsession is None:
            raise DBAPIError

        return request.dbsession.query(cls).get(pk).delete()

