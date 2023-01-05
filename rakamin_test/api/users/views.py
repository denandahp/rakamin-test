from django.forms.models import model_to_dict

from rest_framework import request, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from rakamin_test.api.response import ErrorResponse
from rakamin_test.api.users.serializers import UserSerializers
from rakamin_test.apps.users.model import users
from rakamin_test.core.utils import PaginatorPage

class DetailUsers(APIView):
    authentication_classes = [TokenAuthentication]
    '''
    url= http://127.0.0.1:8000/api/users/detail?mobile_number=081215712199
    :param mobile_number: mobile_number user, must integer
    '''

    def get(self, request: request) -> Response:
        mobile_number = request.GET.get('mobile_number')
        if mobile_number:
            user = users.objects.filter(mobile_number=mobile_number).first()
            if not user:
                data ={
                    'messages': f'Mobile number {mobile_number} not found',
                    'is_success': False
                }
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

            data ={
                'messages': f'Detail user {user}',
                'is_success': True,
                'data': model_to_dict(user)
            }
            return Response(data=data, status=status.HTTP_200_OK)

        return data


class IndexUsers(APIView):
    # Not require token for access
    authentication_classes = []
    permission_classes = []
    '''
    url= http://127.0.0.1:8000/api/users?page=1&limit=10
    :param page: Number of page
    :param limit: Number of page
    '''

    def get(self, request: request) -> Response:
        user_list = []
        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 1))
        users_query = users.objects.all()
        paginator = PaginatorPage(users_query, page, step=limit)
        for user in paginator.objects:
            user_list.append(model_to_dict(user))
        data = {
            'limit': limit,
            'paginator': {
                'next': paginator.next,
                'previous': paginator.previous
            },
            'data': user_list
        }
        return Response(data=data, status=status.HTTP_200_OK)


class CreateUsers(APIView):
    # Not require token for access
    authentication_classes = []
    permission_classes = []
    '''
    url= http://127.0.0.1:8000/api/users/add
    Payload=
        {
            "name": "Pratama",
            "password": "12345678",
            "mobile_number": "081215712196"
        }
    Response=
        {
            "messages": "User Pratama created",
            "data": {
                "name": "Pratama",
                "password": "pbkdf2_sha256$260000$ICKe2djavgy7oSSoYZvz1T$V8LyS4xjV+8+tpgCK7kFhmhsxEFh3f1fkQVCRbx6bLI=",
                "mobile_number": "081215712196"
            },
            "is_success": true
        }
    '''

    def post(self, request: request) -> Response:
        serializer = UserSerializers(data=request.data or None)
        if serializer.is_valid():
            serializer.save()
            user = serializer.data
            data ={
                'messages': f'User {user.get("name")} created',
                'data': user,
                'is_success': True
            }
            return Response(data=data, status=status.HTTP_200_OK)
        return ErrorResponse(serializer=serializer)