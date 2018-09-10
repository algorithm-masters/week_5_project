from marshmallow_sqlalchemy import ModelSchema
from marshmallow_sqlalchemy.fields import fields
from . import NLTKOutput
from . import AccountRole
from . import Account


class AccountRoleSchema(ModelSchema):
    """ Account Role Schema for the db
    """
    class Meta:
        model = AccountRole


class AccountSchema(ModelSchema):
    """ Account Schema for the db
    """
    roles = fields.Nested(AccountRoleSchema, many=True, only='name')

    class Meta:
        model = Account


class NltkResultsSchema(ModelSchema):
    """  Schema for the db
    """
    roles = fields.Nested(AccountRoleSchema, many=True, only='name')
    account = fields.Nested(AccountSchema, exclude=(
        'password', 'nltk_result' 'roles', 'date_created', 'date_updated'))

    class Meta:
        model = NLTKOutput
