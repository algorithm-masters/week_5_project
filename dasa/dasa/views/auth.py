from pyramid_restful.viewsets import APIViewSet
from sqlalchemy.exc import IntegrityError
from pyramid.response import Response
from ..models import Account
import json


class AuthAPIViewset(APIViewSet):
    def create(self, request, auth=None):
        """Create a Auth instance for the user's account"""
        data = json.loads(request.body)

        if auth == 'register':
            try:
                user = Account.new(request, data['email'], data['password'])
            except (IntegrityError, KeyError):
                return Response(json='Bad Request', status=400)

            return Response(
                json_body={
                   'token': request.create_jwt_token(
                        user.email,
                        roles=[role.name for role in user.roles],
                        userName=user.email,
                    )
                },
                status=201
            )

        if auth == 'login':
            authenticated = Account.check_credentials(request, data['email'], data['password'])

            if authenticated:
                return Response(
                    json_body={
                        'token': request.create_jwt_token(
                            authenticated.email,
                            roles=[role.name for role in authenticated.roles],
                            userName=authenticated.email,
                            expiration=1500,
                        )
                    }
                )
            return Response(json='Not Authorized', status=401)

        return Response(json='Not Found', status=404)


