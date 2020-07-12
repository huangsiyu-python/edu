import re

from django.contrib.auth.hashers import make_password
from django_redis import get_redis_connection
from rest_framework import serializers

from user.models import UserInfo
from user.utils import get_user_by_account


class UserModelSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=1024, read_only=True, help_text="用户token")
    sms_code = serializers.CharField(min_length=4, max_length=6, required=True, write_only=True, help_text="短信验证码")

    class Meta:
        model = UserInfo
        fields = ("id", "username", "password", "phone", "token", "sms_code")

        extra_kwargs = {
            "id": {
                'read_only': True,
            },
            "username": {
                "read_only": True,
            },
            "password": {
                "write_only": True,
            },
            "phone": {
                "write_only": True
            }
        }

    def validate(self, attrs):
        phone = attrs.get("phone")
        password = attrs.get("password")
        sms_code = attrs.get("sms_code")

        if not re.match(r'^1[3-9]\d{9}$', phone):
            raise serializers.ValidationError("手机号格式错误")

        try:
            user = get_user_by_account(phone)
        except:
            user = None
        if user:
            raise serializers.ValidationError("当前手机号已经被注册")

        redis_connection = get_redis_connection("sms_code")
        phone_code = redis_connection.get("mobile_%s" % phone)
        print(phone_code)
        if phone_code.decode() != sms_code:
            raise serializers.ValidationError("验证码不一致")

        return attrs

    def create(self, validated_data):

        pwd = validated_data.get("password")
        hash_password = make_password(pwd)
        username = validated_data.get("phone")

        user = UserInfo.objects.create(
            phone=username,
            username=username,
            password=hash_password,
        )

        from rest_framework_jwt.settings import api_settings
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        user.token = jwt_encode_handler(payload)
        print(user)
        return user
