from apps.globals.routines.worker_status.models import WorkerStatus
from lib.base.repositories import BaseRepository


class WorkerStatusRepository(BaseRepository):
    model_class = WorkerStatus

    @staticmethod
    def get_by_worker_type(worker_type: int) -> WorkerStatus:
        return WorkerStatus.objects.get(worker_type=worker_type)
