from pyramid.response import Response
from pyramid.view import view_config
#
# from sqlalchemy.exc import DBAPIError





@view_config(route_name='home', renderer='json', request_method='GET')
def lookup(request):
    """This is going to listen to a request from a specific endpoint.
    """

    response = 'This route works!!'

    return Response(body=response, content_type='text/plain', status=200)
