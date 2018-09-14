from pyramid_restful.viewsets import APIViewSet
from sqlalchemy.exc import IntegrityError, DataError
from pyramid.view import view_config
from pyramid.response import Response
from ..models.nltk_output import NLTKOutput
from ..models.account import Account
from .chart_logic import stacked_bar_for_all, stacked_bar_for_one, pie_for_all
import requests
import json
import html


class NLTKAPIAdmin(APIViewSet):
    """This will create the endpoints to visualize the data that has already
    been created within the database.
    """

    # @detail_route(methods=['get'])
    def retrieve(self, request, graph_type=None, id=None):
        """This retrieves a single users data by email, and displays it with the
        given chart type
        """
        user = {}
        if request.authenticated_userid:
            account = Account.one(request, request.authenticated_userid)
            user['account_id'] = account.id
        if account.check_admin(request, user):
            if graph_type == 'stacked_bar':
                cleaned_data = {}
                raw_data = NLTKOutput.all(request)
                for record in raw_data:
                    if record.account_id == int(id):
                        if record.account_id in cleaned_data:
                            cleaned_data[record.account_id].append(record.nltk_result)
                        else:
                            cleaned_data[record.account_id] = [record.nltk_result]
        return_obj = stacked_bar_for_one(cleaned_data)
        return Response(return_obj.encode(), status=200)

    # @list_route(methods=['get'])
    def list(self, request, graph_type=None):
        """This performs a get all request, which gets all the user data in the database,
        converts it to the type of graph that is requested, and returns html containing that
        graph.
        """
        user = {}
        if request.authenticated_userid:
            account = Account.one(request, request.authenticated_userid)
            user['account_id'] = account.id
        if account.check_admin(request, user):
            cleaned_data = {}
            raw_data = NLTKOutput.all(request)
            for record in raw_data:
                if record.account_id in cleaned_data:
                    cleaned_data[record.account_id].append(record.nltk_result)
                else:
                    cleaned_data[record.account_id] = [record.nltk_result]
            if graph_type == 'stacked_bar':
                return_obj = stacked_bar_for_all(cleaned_data)
            if graph_type == 'pie':
                return_obj = pie_for_all(cleaned_data)
        return Response(return_obj.encode(), status=200)

    def delete(self, request, user_id=None):
        """ Admins are able to delete a user based on the provided id
        """
        data = json.loads(request.body.decode())
        authenticated = Account.check_credentials(request, data['email'], data['password'])
        user = {}
        user['account_id'] = authenticated.id

        if authenticated.check_admin(request, user):
            NLTKOutput.remove(request=request, pk=user_id)
            Account.remove(request=request, pk=user_id)
            return Response(json='Account and content deleted', status=204)

        return Response(json='Not Authorized', status=401)

