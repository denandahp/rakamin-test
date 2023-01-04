from django.forms.models import model_to_dict

from rakamin_test.api.response import ErrorResponse

from rest_framework import request, status
from rest_framework.response import Response
from rest_framework.views import APIView

from rakamin_test.api.users.serializers import UserSerializers
from rakamin_test.apps.users.model import users
from rakamin_test.core.utils import PaginatorPage

class DetailUsers(APIView):
    '''
    url= http://127.0.0.1:8000/api/users/detail?acc_number=1
    :param acc_number: account number user
    '''

    def get(self, request: request) -> Response:
        mobile_number = request.GET.get('mobile_number')
        if mobile_number:
            user = users.objects.filter(mobile_number=mobile_number).first()
            serializer = UserSerializers(user, many=True)
            if not serializer:
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
    '''
    url= http://127.0.0.1:8000/api/users?page=1&limit=10
    :param page: Number of page
    :param limit: Number of page
    '''

    def get(self, request: request) -> Response:
        user_list = []
        limit = int(request.GET.get('limit', 1))
        users = users.objects.all()
        serializer = UserSerializers(users, many=True)
        paginator = PaginatorPage(serializer, request.GET.get('page', 1), step=limit)
        for user in paginator.objects:
            user_list.append(user)
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