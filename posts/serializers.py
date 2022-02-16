from django.db.models import fields
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from knox.models import AuthToken
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


from .models import *

User = get_user_model()

class TokenSerializer(serializers.ModelSerializer):
    class Meta:
      model = AuthToken
      fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("password", "last_login", "date_joined")


class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('id', 'username', 'email')


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('username', 'password', 'email')


    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )

        
        user.set_password(validated_data['password'])
        user.save()

        return user


class LoginSerializer(serializers.Serializer):
  username = serializers.CharField()
  password = serializers.CharField()

  def validate(self, data):
    user = authenticate(**data)
    if user and user.is_active:
      return user
    raise serializers.ValidationError("Incorrect Credentials")


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        exclude = ['user']