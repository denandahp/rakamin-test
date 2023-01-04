from django.urls import include, path


app_name = 'api'

urlpatterns = [
    path('users/', include(
        'rakamin_test.api.users.urls', namespace='users')),
    path('auth/', include(
        'rakamin_test.api.auth.urls', namespace='auth')),
    path('chats/', include(
        'rakamin_test.api.chats.urls', namespace='chats')),
]
