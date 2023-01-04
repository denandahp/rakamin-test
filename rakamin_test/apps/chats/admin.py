from django.contrib import admin

from rakamin_test.apps.chats.model import messages, room

admin.site.register(messages)
admin.site.register(room)
