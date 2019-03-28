from datetime import datetime, timedelta
from typing import List, Tuple

from django.db import transaction, IntegrityError

from apps.domains.account.dtos import UserDto
from apps.domains.account.models import User, UserModifiedHistory
from apps.domains.account.repositories import UserRepository, UserModifiedHistoryRepository
from apps.globals.routines.worker_status.constants import WorkerType
from apps.globals.routines.worker_status.repositories import WorkerStatusRepository
from infra.storage.database.constants import Database
from lib.decorators.dtos import as_dtos
from lib.decorators.retry import retry
from lib.ridibooks.api.store_user import StoreUserApi
from lib.utils.array import to_dict

STORE_API_LIMIT = 64


class CrawlStoreUserService:
    @classmethod
    def crawl(cls):
        worker_status = WorkerStatusRepository.get_by_worker_type(WorkerType.STORE_USER_CRAWLER)

        last_date = cls._get_last_date(worker_status.last_date)
        store_updated_user_idxes = cls._get_store_updated_user_idxes(last_date)

        cls._save_created_or_changed_users(store_updated_user_idxes)

        worker_status.last_date = last_date
        worker_status.save()

    @classmethod
    @transaction.atomic(using=Database.DEFAULT)
    def _save_created_or_changed_users(cls, store_updated_user_idxes: List[int], limit=STORE_API_LIMIT):
        offset = 0
        while True:
            if offset > len(store_updated_user_idxes):
                break
            users_to_create, users_to_update = cls._get_users_to_create_or_update(store_updated_user_idxes[offset:offset + limit])
            cls._create_users(users_to_create)
            cls._update_users(users_to_update)

            offset += limit

    @staticmethod
    def _get_last_date(worker_last_date: datetime) -> datetime:
        # store 에서 기준 시간으로부터 5분전의 히스토리까지를 받아 올 수 있어서 5분 간격으로 요청한다. 단 전에 실행한 시간과 현재의 간격이 5분보다 작다면 현재시간으로 진행한다.
        last_date = worker_last_date + timedelta(minutes=5)
        return last_date if last_date < datetime.now() else datetime.now()

    @staticmethod
    def _get_store_updated_user_idxes(last_date: datetime) -> List[int]:
        response = StoreUserApi().get_updated_user_idxes_by_before(last_date)
        return list(set([user['u_idx'] for user in response['users']]))

    @staticmethod
    @as_dtos(UserDto)
    def _get_store_user_dtos(user_idxes: List[int]) -> List[UserDto]:
        return StoreUserApi().get_users_by_idxes(user_idxes)

    @staticmethod
    def _create_user_from_dto(user_dto: UserDto) -> User:
        return User(
            idx=user_dto.u_idx,
            id=user_dto.u_id,
            name=user_dto.name,
            reg_date=user_dto.reg_date,
            ip=user_dto.ip,
            device_id=user_dto.device_id,
            email=user_dto.email,
            birth_date=user_dto.birth_date,
            gender=user_dto.gender,
            verified=user_dto.verified,
            status=user_dto.status,
            email_verify_date=user_dto.email_verify_date,
            last_modified=user_dto.updated_at
        )

    @classmethod
    def _get_users_to_create_or_update(cls, store_updated_user_idxes: List[int]) -> Tuple[List[User], List[User]]:
        store_user_dtos = cls._get_store_user_dtos(store_updated_user_idxes)
        existing_users_dict = to_dict(UserRepository.find_by_u_idxes(store_updated_user_idxes), 'idx')

        users_to_create = []
        users_to_update = []

        for store_user_dto in store_user_dtos:
            user = cls._create_user_from_dto(store_user_dto)

            if user.idx not in existing_users_dict:
                users_to_create.append(user)

            elif user != existing_users_dict[user.idx]:
                users_to_update.append(user)

        return users_to_create, users_to_update

    @classmethod
    @retry(retry_count=3, retriable_exceptions=IntegrityError)
    def _create_users(cls, users: List[User]):
        cls._create_user_modified_histories_by_users(users)
        UserRepository.create(users)

    @classmethod
    def _update_users(cls, users: List[User]):
        cls._create_user_modified_histories_by_users(users)
        UserRepository.update(users)

    @staticmethod
    def _create_user_modified_histories_by_users(users: List[User]):
        user_modified_histories = []
        for user in users:
            user_modified_histories.append(UserModifiedHistory(u_idx=user.idx))
        UserModifiedHistoryRepository.create(user_modified_histories, True)
