from django.db import models

from apps.globals.routines.worker_status.constants import WorkerType
from lib.django.db.models.base_model import BaseModel


class WorkerStatus(BaseModel):
    worker_type = models.IntegerField(unique=True, choices=WorkerType.get_choices(), verbose_name='worker_type', )
    last_date = models.DateTimeField(verbose_name='last_date')

    class Meta:
        db_table = 'worker_status'
