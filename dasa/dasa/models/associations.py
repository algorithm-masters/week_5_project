from sqlalchemy import Table, Column, Integer, ForeignKey
from .meta import metadata


roles_association = Table(
    'roles_association',
    metadata,
    Column('account_id', Integer, ForeignKey('accounts.id', ondelete='CASCADE')),
    Column('role_id', Integer, ForeignKey('account_roles.id', ondelete='CASCADE'))
)
