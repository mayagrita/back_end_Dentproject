from django.urls import path
from users.views import UserList,LoginAPI,RegisterAPI,LogoutAPI

urlpatterns = [
    path('users/', UserList.as_view(), name='user-list'),
    path('login/', LoginAPI.as_view(), name='Login'),
    path('register/', RegisterAPI.as_view(), name='register'),
    path('logout/', LogoutAPI.as_view(), name='logout'),
]