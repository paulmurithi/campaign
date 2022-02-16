from django.contrib import admin
from django.urls import path, include

from .views import PostViewSet, Register, Login_View, User_View, ShowProfile
from knox import views as knox_views

# rest imports
from rest_framework import routers

router = routers.DefaultRouter()
router.register("posts", PostViewSet)

urlpatterns = [
    path('api/auth', include('knox.urls')),
    path('auth/register/', Register.as_view(), name="register"),
    path("auth/login/", Login_View.as_view()),
    path("auth/user/", User_View.as_view(), name="user"),
    path("profile/", ShowProfile.as_view(), name="profile"),
    path("auth/logout/", knox_views.LogoutView.as_view(), name='knox_logout'),
    path("", include(router.urls)),
]
