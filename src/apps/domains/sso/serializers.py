from rest_framework import serializers

from apps.domains.sso.constants import SSOKeyHint
from lib.base.serializers import BaseSerializer


class BaseSSOSerializer(BaseSerializer):
    hint = serializers.ChoiceField(choices=SSOKeyHint.get_choices(), required=True, label='SSO Key 힌트')


class GenerateTokenRequestSerializer(BaseSSOSerializer):
    pass


class GenerateTokenResponseSerializer(BaseSerializer):
    token = serializers.CharField(required=True, label='SSO 토큰')


class VerifyTokenRequestSerializer(BaseSSOSerializer):
    token = serializers.CharField(required=True, label='SSO 토큰')


class VerifyTokenResponseSerializer(BaseSerializer):
    u_idx = serializers.IntegerField(required=True, label='유저 Idx')
