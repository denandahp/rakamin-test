from django.urls import path

from rakamin_test.api.auth.views import Login, Logout

app_name = 'auth'


urlpatterns = [
    path('login', Login.as_view(), name="login"),
    path('logout', Logout.as_view(), name="logout"),
]
