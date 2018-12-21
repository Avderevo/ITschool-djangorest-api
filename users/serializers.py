from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import User
from users.models import Activation, Profile
from ITS_api import settings
from .mail_sender import send_confirm_email
from django.contrib.auth.tokens import default_token_generator as dtg


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('__all__')


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ('username', 'id', 'email', 'is_active', 'profile')


class UserSerializerWithToken(serializers.ModelSerializer):

    token = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    def get_token(self, obj):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        return token

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = self.Meta.model(**validated_data)
        if password is not None:
            user.set_password(password)
        if settings.USER_EMAIL_ACTIVATION:
            user.is_active = False
            code = dtg.make_token(user)
            act = Activation()
            act.code = code
            act.user = user
            send_confirm_email(user.email, code)

        user.save()
        return user

    class Meta:
        model = User
        fields = ('token', 'username', 'password', 'email')


