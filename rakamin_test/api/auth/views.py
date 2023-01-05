from django.contrib.auth import login, logout, authenticate
from django.core.exceptions import ObjectDoesNotExist

from rakamin_test.core.utils import AuthBackend

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView


class Login(APIView):
    authentication_classes = []
    permission_classes = []
    '''
    url= http://127.0.0.1:8000/api/auth/login
    Payload = 
        {
            "mobile_number": "081215712199",
            "password": "12345678"
        }
    Response=
        {
            "data": {
                "name": "081215712199",
                "mobile_number": "081215712199",
                "is_superuser": true
            },
            "token": "42be397d4a17e39205782db741c92832652d5a59"
        }
    '''

    def post(self, request):
        mobile_number = request.data.get('mobile_number')
        password = request.data.get('password')
        user = AuthBackend.authenticate(username=mobile_number, password=password)
        if user and user.is_active:
            login(request, user)
            token = Token.objects.get_or_create(user=user)
            token_key = token[0].key
            response = self.response_login(user)
            response_dict = {
                "data": response,
                "token": token_key
            }
            return Response(response_dict, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Login Failed"}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        return Response({"message": "Now Login"}, status=status.HTTP_200_OK)
    
    def response_login(self, user):
        data = {
            "name": user.name,
            "mobile_number": user.mobile_number,
            "is_superuser": False,
        }

        if user.is_superuser or user.is_supervisor:
            data['is_superuser'] = True
            return data
        return data


class Logout(APIView):
    authentication_classes = []
    permission_classes = []
    '''
    url= http://127.0.0.1:8000/api/auth/logout
    response=
        {
            "success": "logout success."
        }
    '''

    def get(self, request):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass

        logout(request)
        return Response({"success": "logout success."}, status=status.HTTP_200_OK)
