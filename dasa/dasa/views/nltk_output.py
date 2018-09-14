from pyramid_restful.viewsets import APIViewSet
from sqlalchemy.exc import IntegrityError, DataError
from pyramid.view import view_config
from pyramid.response import Response
from ..models.nltk_output import NLTKOutput
from ..models.account import Account
# from .chart_logic import chart_for_one_user
import requests
import json


class NLTKAPIView(APIViewSet):
    '''This class displays the api endpoint message. It is not built out yet, as it needs
    actual functionality besides just sending jsons.
    '''

    def create(self, request):
        """This performs a POST request for a new nltk analysis.
        """
        try:
            kwargs = json.loads(request.body.decode())
        except json.JSONDecodeError as e:
            return Response(json=e.msg, status=400)

        if 'text' not in kwargs:
            return Response(json='Expected value: text', status=400)

        if request.authenticated_userid:
            account = Account.one(request, request.authenticated_userid)
            kwargs['account_id'] = account.id
            
        try:
            analysis = NLTKOutput.new(request, **kwargs)
        except IntegrityError:
            return Response(json='Duplicate Key Error. Analysis already exists', status=409)
        
        return Response(json=analysis[1], status=201)
