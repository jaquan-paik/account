from rest_framework import serializers

from apps.domains.oauth2.constants import GrantType
from lib.base.serializers import BaseSerializer


class GrantTypeSerializer(BaseSerializer):
    grant_type = serializers.ChoiceField(required=True, choices=GrantType.SUPPORTED_LIST)


class ClientConfidentialSerializer(BaseSerializer):
    client_id = serializers.CharField(required=True)
    client_secret = serializers.CharField(required=True)


class AuthorizationCodeGrantSerializer(ClientConfidentialSerializer):
    code = serializers.CharField(required=True)
    redirect_uri = serializers.URLField(required=True)


class RefreshTokenGrantSerializer(ClientConfidentialSerializer):
    refresh_token = serializers.CharField(required=True)


class PasswordGrantSerializer(ClientConfidentialSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
