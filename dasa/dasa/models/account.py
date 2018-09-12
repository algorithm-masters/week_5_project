from .meta import Base
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import relationship
from .associations import roles_association
from .role import AccountRole
from datetime import datetime as dt
from cryptacular import bcrypt
from .nltk_output import NLTKOutput

from sqlalchemy import (
    Column,
    Index,
    Integer,
    String,
    Text,
    DateTime,
)

manager = bcrypt.BCRYPTPasswordManager()


class Account(Base):
    """Create a table for the accounts
    """
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True)
    email = Column(Text, nullable=False, unique=True)
    password = Column(Text, nullable=False)
    # name this something nltk related -- check that
    nltk_output = relationship(NLTKOutput, back_populates='accounts')
    
    account_roles = relationship('AccountRole', secondary=roles_association, back_populates='accounts')
    date_created = Column(DateTime, default=dt.now())
    date_updated = Column(DateTime, default=dt.now(), onupdate=dt.now())

    def __init__(self, email=None, password=None):
        """Initilize a new user
        """
        self.email = email
        self.password = manager.encode(password, 10)


    @classmethod
    def new(cls, request, email=None, password=None):
        """ Create a new user, give them a role, and put it in the db,
        """
        if request.dbsession is None:
            raise DBAPIError

        user = cls(email, password)
        request.dbsession.add(user)

        # adding role to the user
        # this is unsafe
        admin_role = request.dbsession.query(AccountRole).filter(
            AccountRole.name == 'admin').one_or_none()

        user.account_roles.append(admin_role)
        request.dbsession.flush()

        # this line adds the user to the database:
        return request.dbsession.query(cls).filter(
            cls.email == email).one_or_none()

    @classmethod
    def one(cls, request, email=None):
        """ Return one account based on the logged in users email address
        """
        return request.dbsession.query(cls).filter(
            cls.email == email).one_or_none()

    @classmethod
    def check_credentials(cls, request, email, password):
        """ Validate that the user exsists and that they are who theyclaim to be
        """
        # TODO: Complete this tomorrow as part of the login process
        if request.dbsession is None:
            raise DBAPIError
        try:
            account = request.dbsession.query(cls).filter(
                cls.email == email).one_or_none()
        except DBAPIError:
            return None

        if account is not None:
            if manager.check(account.password, password):
                return account

        return None
