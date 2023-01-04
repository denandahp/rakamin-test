from django.urls import path

from rakamin_test.api.users.views import (
    CreateUsers, IndexUsers, DetailUsers)

app_name = 'users'

urlpatterns = [
    path('', IndexUsers.as_view(), name="index_user"),
    path('detail', DetailUsers.as_view(), name="detail_user"),
    path('add', CreateUsers.as_view(), name="create_user")
]
