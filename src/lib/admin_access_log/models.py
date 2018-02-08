from django.db import models

from lib.django.db.models.base_model import BaseModel
from .constants import RequestMethod


class AdminUrlAccessHistory(BaseModel):
    staff_id = models.IntegerField(db_index=True, verbose_name='Staff')
    method = models.IntegerField(db_index=True, choices=RequestMethod.get_choices(), verbose_name='method')
    url = models.CharField(db_index=True, max_length=200, verbose_name='url')

    class Meta:
        db_table = 'admin_url_access_history'
        verbose_name = 'Admin 접근 로그'
        verbose_name_plural = 'Admin 접근 로그 리스트'

    @staticmethod
    def create(staff_id: int, method: int, url: str):
        return AdminUrlAccessHistory(staff_id=staff_id, method=method, url=url)
