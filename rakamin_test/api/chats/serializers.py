from rest_framework import serializers

from django.db.models import Q

from rakamin_test.apps.chats.model import messages, room


class MessagesSerializers(serializers.ModelSerializer):
    class Meta:
        model = messages
        fields = ['sender', 'receiver', 'message', 'reply_from']
    
    def validate_message(self, message):
        if not message:
             raise serializers.ValidationError('This field must be an even number.')
        return message

    def create(self, validated_data):
        sender = validated_data.get('sender', '')
        receiver = validated_data.get('receiver', '')

        room_exist = room.objects.filter(
            Q(user1=sender, user2=receiver) | 
            Q(user2=sender, user1=receiver)).first()
        if not room_exist:
            room_exist = room.objects.create(user1=sender, user2=receiver)
        message = messages.objects.create(**validated_data)
        message.room = room_exist
        message.save()

        return message
    
    def update(self, instance, validated_data):
        unread_messages_list = []
        for unread_message in instance:
            unread_message.is_read = validated_data.get('is_read')
            unread_messages_list.append(unread_message)
        messages.objects.bulk_update(unread_messages_list, ['is_read'])
        return instance



class RoomSerializers(serializers.ModelSerializer):
    class Meta:
        model = room
        fields = ['user1', 'user2', 'name']