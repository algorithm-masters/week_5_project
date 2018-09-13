from pyramid_restful.viewsets import APIViewSet
from sqlalchemy.exc import IntegrityError
from pyramid.response import Response
from ..models.account import Account
from ..models.nltk_output import NLTKOutput
import json


class AuthAPIView(APIViewSet):
    def create(self, request, auth=None):
        """Create a Auth instance for the user's account"""

        data = json.loads(request.body.decode())
        if auth == 'register':
            try:
                user = Account.new(request, data['email'], data['password'])
            except (IntegrityError, KeyError):
                return Response(json='Bad Request', status=400)

            return Response(
                json_body={
                   'token': request.create_jwt_token(
                        user.email,
                        roles=[role.name for role in user.account_roles],
                        userName=user.email,
                        expiration=345600
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
                            roles=[role.name for role in authenticated.account_roles],
                            userName=authenticated.email,
                            expiration=345600,
                        )
                    }
                )
            return Response(json='Not Authorized', status=401)

        if auth == 'delete':
            authenticated = Account.check_credentials(request, data['email'], data['password'])

            if authenticated:
                # import pdb; pdb.set_trace()
                NLTKOutput.remove(request=request, pk=authenticated.id)
                # import pdb; pdb.set_trace()
                Account.remove(request=request, pk=authenticated.id)
                return Response(json='Account and content deleted', status=204)
            
            return Response(json='Not Authorized', status=401)

        return Response(json='Not Found', status=404)




# def destroy(self, request, id=None):
        # """
        # """
        # if not request.authenticated_userid:
        #     return Response(json='Forbidden', status=403)

        # if not id:
        #     return Response(json='Not Found', status=404)

        # try:
        #     WeatherLocation.remove(request=request, pk=id)
        # except (DataError, AttributeError):
        #     return Response(json='Not Found', status=404)

        # return Response(status=204)