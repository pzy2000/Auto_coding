from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .helpers import *
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True)
    password_confirmation = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password_confirmation')

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('User already exist')
        return email

    def validate(self, validation_data):
        password = validation_data.get('password')
        password_confirmation = validation_data.pop('password_confirmation')
        if password != password_confirmation:
            raise serializers.ValidationError('Password Error')
        return validation_data

    def create(self, validated_data):
        email = validated_data.get('email')
        password = validated_data.get('password')
        user = User.objects.create_user(email, password)
        send_activation_email(user.email, user.activation_code)
        return user


class ActivationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    activation_code = serializers.CharField(min_length=8)

    def validate(self, attrs):
        email = attrs.get('email')
        activation_code = attrs.get('activation_code')

        if not User.objects.filter(email=email, activation_code=activation_code).exists():
            raise serializers.ValidationError('User is nor found!')
        return attrs

    def activate(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        user.is_active = True
        user.activation_code = ''
        user.save()


class LoginSerializer(TokenObtainPairSerializer):
    pass


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("full_name", "groups", "username")


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", 'full_name', "date_joined")


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("full_name", )


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError as exc:
            self.fail('bad_token')