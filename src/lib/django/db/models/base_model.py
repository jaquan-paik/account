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
