from pyramid_restful.viewsets import APIViewSet
from sqlalchemy.exc import IntegrityError, DataError
from pyramid.view import view_config
from pyramid.response import Response
from ..models.nltk_output import NLTKOutput
from ..models.account import Account
from ..models.schemas import AccountSchema
import requests
import json


class GetAPIUsers(APIViewSet):
    def list(self, request):
        user = {}
        if request.authenticated_userid:
            account = Account.one(request, request.authenticated_userid)
            user['account_id'] = account.id
        
        if account.check_admin(request, user):
            email_list = Account.all(request)
            schema = AccountSchema()
            data = [schema.dump(email).data['email'] for email in email_list]
            return Response(json=data, status=200)
        return Response(json='Not Authorized', status=401)
