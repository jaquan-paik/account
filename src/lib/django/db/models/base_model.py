from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.db.models import Manager


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='등록일')
    last_modified = models.DateTimeField(auto_now=True, editable=False, verbose_name='수정일')

    objects = Manager()

    class Meta:
        abstract = True


class BaseUserModel(BaseModel, AbstractBaseUser):
    class Meta:
        abstract = True


class EqualizeMixin:
    equal_fields = ()

    def __eq__(self, other):
        equal_fields = self._get_equal_fields()
        for field in equal_fields:
            if getattr(self, field) != getattr(other, field):
                return False
        return True

    def _get_equal_fields(self):
        if not self.equal_fields:
            raise NotImplementedError()

        return self.equal_fields

    def merge(self, other):
        equal_fields = self._get_equal_fields()
        for field in equal_fields:
            if getattr(self, field) != getattr(other, field):
                setattr(self, field, getattr(other, field))
