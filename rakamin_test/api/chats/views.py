
from django.db.models import Q
from django.forms.models import model_to_dict

from rest_framework import request, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from rakamin_test.api.response import ErrorResponse
from rakamin_test.api.chats.serializers import MessagesSerializers, RoomSerializers
from rakamin_test.apps.chats.model import messages, room
from rakamin_test.core.utils import PaginatorPage


class SendMessages(APIView):
    authentication_classes = [TokenAuthentication]
    '''
    url= http://127.0.0.1:8000/api/chats/send_messages
    headers = {'Authorization': 'Token 42be397d4a17e39205782db741c92832652d5a59'}
    payload= 
        JSON data to send message to other user
        {
            "receiver": 3,                # Id User must integer
            "message": "cek Halo 1 2 3",  # Text message must string 
        }

        JSON data to reply previous message
        {
            "receiver": 3,                # Id User must integer
            "message": "cek Halo 1 2 3",  # Text message must string 
            "reply_from": 4               # Id message must integer 
        }
    Response=
        {
            "Sender": "081215712199",
            "messages": "Send messages success",
            "is_success": true,
            "data": {
                "receiver": 3,
                "message": "ok",
                "reply_from": null
            }
        }
    '''

    def post(self, request: request) -> Response:
        user_sender = request.user
        serializer = MessagesSerializers(data=request.data or None)
        if serializer.is_valid():
            serializer.save(sender=user_sender)
            chat = serializer.data

            data ={
                'Sender': user_sender.name,
                'messages': f'Send messages success',
                'is_success': True,
                'data': chat
            }
            return Response(data=data, status=status.HTTP_200_OK)
        return ErrorResponse(serializer=serializer)


class IndexRoom(APIView):
    authentication_classes = [TokenAuthentication]

    '''
    url= http://127.0.0.1:8000/api/chats/room?page=1&limit=5
    headers = {'Authorization': 'Token 42be397d4a17e39205782db741c92832652d5a59'}
    :param page: Number of page
    :param limit: Limit data per page
    '''

    def get(self, request: request) -> Response:
        if not request.auth:
            return Response(data={'detail': 'unauthorization'}, status=status.HTTP_400_BAD_REQUEST)
        user_id = request.user.id
        limit = int(request.GET.get('limit', 1))
        page = request.GET.get('page', 1)
        room_list = []
        room_query = room.objects.select_related('user1').filter(Q(user1=user_id) | Q(user2=user_id))
        paginator = PaginatorPage(room_query, page, step=limit)
        for rooms in paginator.objects:
            name_receiver = None
            if rooms.user1.id == user_id:
                name_receiver = rooms.user2.name
            else:
                name_receiver = rooms.user1.name
            message = messages.objects.select_related('sender').filter(room=rooms)
            unread_count = message.filter(is_read=False).count() if message.filter(is_read=False, receiver_id=user_id) else 0
            room_list.append({
                'id': rooms.id,
                'name': name_receiver,
                'last_messages': message.last().message,
                'unread_count': unread_count
            })

        data = {
            'limit': limit,
            'paginator': {
                'next': paginator.next,
                'previous': paginator.previous
            },
            'data': room_list
        }
        return Response(data=data, status=status.HTTP_200_OK)


class IndexMessages(APIView):
    authentication_classes = [TokenAuthentication]
    '''
    url= http://127.0.0.1:8000/api/chats/messages?page=1&limit=5&room=2
    headers = {'Authorization': 'Token 42be397d4a17e39205782db741c92832652d5a59'}
    :param page: Number of page, must integer
    :param limit: Limit data per page, must integer
    :param room: Id room, must integer
    '''

    def get(self, request: request) -> Response:
        if not request.auth:
            return Response(data={'detail': 'unauthorization'}, status=status.HTTP_400_BAD_REQUEST)
        user_id = request.user.id
        limit = int(request.GET.get('limit', 1))
        page = request.GET.get('page', 1)
        room_filter = request.GET.get('room')

        messages_list = []
        message_query = messages.objects.select_related('room').filter(room=room_filter).order_by('-created')
        room_query = message_query.first().room
        name_sender = None
        if room_query.user1.id == user_id:
            name_sender = room_query.user2.id
        else:
            name_sender = room_query.user1.id

        # Update message to read if call this API
        unread_messages = message_query.filter(sender_id=name_sender, is_read=False)
        if unread_messages:
            unread_messages_list = []
            for unread_message in unread_messages:
                unread_message.is_read = True
                unread_messages_list.append(unread_message)
            messages.objects.bulk_update(unread_messages_list, ['is_read'])

        paginator = PaginatorPage(message_query, page, step=limit)
        for message in paginator.objects:
            messages_list.append(model_to_dict(message))

        data = {
            'name': request.user.name,
            'limit': limit,
            'paginator': {
                'next': paginator.next,
                'previous': paginator.previous
            },
            'data': messages_list
        }
        return Response(data=data, status=status.HTTP_200_OK)