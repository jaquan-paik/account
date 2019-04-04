from rest_framework import serializers

from lib.base.serializers import BaseSerializer


class SSOOtpGenerateResponseSerializer(BaseSerializer):
    otp = serializers.CharField(required=True, label='SSO Otp')


class SSOOtpVerifyRequestSerializer(BaseSerializer):
    otp = serializers.CharField(required=True, label='SSO Otp')


class SSOOtpVerifyResponseSerializer(BaseSerializer):
    u_idx = serializers.IntegerField(required=True, label='유저 IDX')
