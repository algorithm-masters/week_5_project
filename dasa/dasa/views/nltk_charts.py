from pyramid_restful.viewsets import APIViewSet
from sqlalchemy.exc import IntegrityError, DataError
from pyramid.view import view_config
from pyramid.response import Response
from ..models.nltk_output import NLTKOutput
from ..models.account import Account
import requests
import json


class NLTKAPICharts(APIViewSet):
    """This will create the endpoints to visualize the data that has already
    been created within the database.
    """

    # def create(self, request):
    #   """This performs a POST request for a new nltk analysis.
    #   """
    #     data = json.loads(request.body.decode())
    #     if graph_type == 'bar':
    #     try:
    #         kwargs = json.loads(request.body.decode())
    #     except json.JSONDecodeError as e:
    #         return Response(json=e.msg, status=400)

    #     if 'text' not in kwargs:
    #         return Response(json='Expected value: text', status=400)

    #     if request.authenticated_userid:
    #         account = Account.one(request, request.authenticated_userid)
    #         kwargs['account_id'] = account.id
            
    #     try:
    #         analysis = NLTKOutput.new(request, **kwargs)
    #     except IntegrityError:
    #         return Response(json='Duplicate Key Error. Analysis already exists', status=409)
    #     # schema = NltkResultsSchema()
    #     # data = schema.dump(analysis).data
    #     return Response(json=analysis[1], status=201)
        

    def list(self, request, graph_type=None):
        """This performs a get all request, which gets all the user data in the database,
        converts it to the type of graph that is requested, and returns html containing that
        graph.
        """
        import pdb; pdb.set_trace()
        user = {}
        if request.authenticated_userid:
            account = Account.one(request, request.authenticated_userid)
            user['account_id'] = account.id
        
        if graph_type == 'stacked_bar':
            cleaned_data = {}
            raw_data = NLTKOutput.all(request)
            for record in raw_data:
                if record.account_id == user.account_id:
                    if record.account_id in cleaned_data:
                        cleaned_data[record.account_id].append(record.nltk_result)
                    else:
                        cleaned_data[record.account_id] = [record.nltk_result]
                
                # Send data to chart maker

        return Response(json=cleaned_data, status=200)
