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
            user_list = Account.all(request)
            schema = AccountSchema()
            emails = [schema.dump(email).data['email'] for email in user_list]
            ids = [schema.dump(user_ids).data['id'] for user_ids in user_list]
            ids_and_emails = {}
            for i in range(len(emails)):
                ids_and_emails[ids[i]] = emails[i]
            return Response(json=ids_and_emails, status=200)
        return Response(json='Not Authorized', status=401)
