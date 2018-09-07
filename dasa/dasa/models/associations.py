from sqlalchemy import Table, Column, Integer, ForeignKey
from .meta import metadata


roles_association = Table(
    'roles_association',
    metadata,
    Column('account_id', Integer, ForeignKey('accounts.id')),
    Column('role_id', Integer, ForeignKey('account_roles.id'))
)