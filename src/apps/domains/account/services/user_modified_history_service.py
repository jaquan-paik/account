from apps.domains.account.repositories import UserModifiedHistoryRepository

PER_ITER_COUNT = 1000


class UserModifiedHistoryService:
    @classmethod
    def set_orders(cls):
        last_ordered_history = UserModifiedHistoryRepository.get_last_ordered()
        order = last_ordered_history.order + 1 if last_ordered_history is not None else 1

        unordered_histories = UserModifiedHistoryRepository.find_unordered(0, PER_ITER_COUNT)

        for unordered_history in unordered_histories:
            unordered_history.order = order
            order += 1

        UserModifiedHistoryRepository.update(unordered_histories, ['order'])
