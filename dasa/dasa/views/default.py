from pyramid.response import Response
from pyramid.view import view_config
from ..models.account import Account


@view_config(route_name='home', renderer='templates/home.jinja2', request_method='GET')
def lookup(request):
    """This is going to listen to a request from a specific endpoint.
    """
    response = 'This is the home page!! It works'
    return {'message': response}




