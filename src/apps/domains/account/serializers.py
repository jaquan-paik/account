from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from apps.domains.account.models import User, UserModifiedHistory
from lib.base.serializers import BaseSerializer


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('idx', 'id')


class MultipleUserRequestSerializer(BaseSerializer):
    u_idxes = serializers.ListField(
        child=serializers.IntegerField(required=True, label='u_idx'), required=True, allow_empty=False, label='u_idx 리스트'
    )
    fields = serializers.ListField(
        child=serializers.CharField(required=True, label='field'), required=False, allow_empty=False, label='응답 필드 리스트'
    )


class MultipleUserResponseSerializer(BaseSerializer):
    def __init__(self, *args, fields=None, **kwargs):
        super().__init__(*args, **kwargs)
        if fields is None:
            fields = []
        self._fields_only = fields

    users = serializers.ListField(child=UserSerializer(), required=True, label='user 리스트')


class UserModifiedHistorySerializer(ModelSerializer):
    class Meta:
        model = UserModifiedHistory
        fields = ('u_idx', 'order', 'last_modified')


class UserModifiedHistoryRequestSerializer(BaseSerializer):
    order = serializers.IntegerField(required=False, default=0, label='히스토리 순서', )
    offset = serializers.IntegerField(required=False, default=0, label='조회 시작 기준 offset', )
    limit = serializers.IntegerField(required=False, default=1000, label='응답 item 개수', )


class UserModifiedHistoryResponseSerializer(BaseSerializer):
    histories = serializers.ListField(child=UserModifiedHistorySerializer(), required=True, label='사용자 정보 변경 리스트')
