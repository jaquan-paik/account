from infra.network.constants.api_status_code import ApiStatusCodes
from lib.log import sentry
from .helper import LockHelper, LockKeyGenerator


def lock(key_prefix=None, lock_ttl=LockHelper.DEFAULT_TTL):
    def _decorator(view_func):
        def _wrapper(self, request, *args, **kwargs):
            customer = request.user
            if not customer.is_authenticated:
                return view_func(self, request, *args, **kwargs)

            lock_helper = LockHelper(LockKeyGenerator.get_api_key_maker(key_prefix, customer.id), lock_ttl)
            if not lock_helper.lock():
                sentry.error_message('[API중복요청] %s - %s' % (request.path, lock_helper.key))
                return self.fail_response(message='중복 요청을 했습니다.', code=ApiStatusCodes.X_400_DUPLICATE_API)

            response = view_func(self, request, *args, **kwargs)

            lock_helper.unlock()
            return response

        return _wrapper
    return _decorator
