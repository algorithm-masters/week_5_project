from ..models.schemas import NltkResultsSchema
from pyramid_restful.viewsets import APIViewSet
from sqlalchemy.exc import IntegrityError, DataError
from pyramid.view import view_config
from pyramid.response import Response
from ..models import NLTKOutput
import requests
import json


# @view_config(route_name='lookup', renderer='json', request_method='GET')
# def lookup(request):
#     """This is going to listen to a request from a specific endpoint.
#     """
#     symbol = request.matchdict['symbol']
#     url = f'{API_URL}stock/{symbol}/company'
#     response = requests.get(url)

#     return Response(json=response.json(), status=200)


class NLTKAPIView(APIViewSet):
    '''This class displays the api endpoint message. It is not built out yet, as it needs
    actual functionality besides just sending jsons.
    '''

    def create(self, request):
        """This performs a POST request for a new nltk analysis.
        """
        try:
            kwargs = json.loads(request.body)
        except json.JSONDecodeError as e:
            return Response(json=e.msg, status=400)

        if 'symbol' not in kwargs:
            return Response(json='Expected value: symbol', status=400)
        try:
            analysis = NLTKOutput.new(request, **kwargs)
        except IntegrityError:
            return Response(json='Duplicate Key Error. Analysis already exists', status=409)

        schema = NltkResultsSchema()
        data = schema.dump(analysis).data

        return Response(json=data, status=201)

    # def retrieve(self, request, id=None):
    #     """This performs a GET request for one stock from the local database.
    #     """
    #     record = StocksInfo.one(request, id)
    #     if not record:
    #         return Response(json='Not Found', status=404)
    #     schema = StocksInfoSchema()
    #     data = schema.dump(record).data

    #     return Response(json=data, status=200)

    # def list(self, request):
    #     """This performs a GET request for all the stocks in the local database.
    #     """
    #     records = StocksInfo.all(request)
    #     schema = StocksInfoSchema()
    #     data = [schema.dump(record) for record in records]

    #     return Response(json=data, status=200)

    # def destroy(self, request, id=None):
    #     """This performs a DELETE request for a single stock in the database.
    #     """
    #     if not id:
    #         return Response(json='Not Found', status=404)

    #     try:
    #         StocksInfo.remove(request=request, pk=id)
    #     except (DataError, AttributeError):
    #         return Response(json='Not Found', status=404)

    #     return Response(status=204)
