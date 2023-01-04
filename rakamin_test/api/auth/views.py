from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist


from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView


class Login(APIView):
    def post(self, request):
        mobile_number = request.data.get('mobile_number')
        password = request.data.get('password')
        user = authenticate(username=mobile_number, password=password)
        print(user)
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
    
    def response_login(user):
        data = {
            "name": user.name,
            "mobile_number": user.email,
            "is_superuser": False,
        }

        if user.is_superuser or user.is_supervisor:
            data['is_superuser'] = True
            return data



class Logout(APIView):
    def get(self, request):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass

        logout(request)
        return Response({"success": "logout success."}, status=status.HTTP_200_OK)
