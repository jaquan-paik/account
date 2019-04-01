from rest_framework import serializers

from lib.base.serializers import BaseSerializer


class GenerateTokenResponseSerializer(BaseSerializer):
    token = serializers.CharField(required=True, label='SSO 토큰')


class VerifyTokenRequestSerializer(BaseSerializer):
    token = serializers.CharField(required=True, label='SSO 토큰')


class VerifyTokenResponseSerializer(BaseSerializer):
    u_idx = serializers.IntegerField(required=True, label='유저 Idx')
