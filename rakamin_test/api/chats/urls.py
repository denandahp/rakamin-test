from django.urls import path

from rakamin_test.api.chats.views import (
    SendMessages, IndexRoom, IndexMessages)

app_name = 'chats'

urlpatterns = [
    path('send_messages', SendMessages.as_view(), name="deposit"),
    path('room', IndexRoom.as_view(), name="inde_room"),
    path('messages', IndexMessages.as_view(), name="inde_room")
]
