from pyramid.response import Response
from pyramid.view import forbidden_view_config, notfound_view_config


@forbidden_view_config()
def forbidden(request):
    return Response(json_body={'message': 'Forbidden Request'}, status=403)


@notfound_view_config()
def not_found(request):
    return Response(json_body={'message': 'Not Found'}, status=404)