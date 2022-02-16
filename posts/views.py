from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication

from .models import Post

# rest imports
from . import serializers

# from rest_framework.authtoken.models import Token
from rest_framework import viewsets, generics
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response

from knox.models import AuthToken
from knox.auth import TokenAuthentication


from django.contrib.auth import  logout


class Register(generics.GenericAPIView):
    serializer_class = serializers.RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        autoken = AuthToken.objects.create(user)
        print(autoken)
        return Response({
        "user": serializers.UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })


class ShowProfile(APIView):
    authentication_classes = [
        TokenAuthentication,
    ]

    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = serializers.UserProfileSerializer(request.user)
        return Response(serializer.data)


class Login_View(generics.GenericAPIView):
    serializer_class = serializers.LoginSerializer
    authentication_classes = [BasicAuthentication]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
        "user": serializers.UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })


class User_View(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated,]
    authentication_classes = [TokenAuthentication,]
    serializer_class = serializers.UserSerializer

    def get_object(self):
        return self.request.user


class Logout_View(APIView):
    permission_classes = [IsAuthenticated,]
    authentication_classes = [TokenAuthentication,]

    def post(self, request):
        logout(request)
        return Response(status=204)


class PostViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Post.objects.filter(approved=True)
    serializer_class = serializers.PostSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

