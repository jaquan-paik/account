from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect

from infra.configure.config import GeneralConfig
from lib.base.exceptions import ErrorException
from lib.utils.url import generate_query_url


class RidiLoginView(LoginView):
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            # 로그인 되어 있으면 Next로 이동한다.
            redirect_to = self.get_success_url()
            if redirect_to == self.request.path:
                raise ErrorException('LOGIN REDIRECT URL IS SAME!')
        else:
            # 로그인 안되어 있으면 리디북스 홈페이지로 이동하고 돌아온다.
            params = {
                'return_url': request.build_absolute_uri()
            }

            redirect_to = generate_query_url(GeneralConfig.get_ridibooks_login_url(), params)

        return HttpResponseRedirect(redirect_to)

    def post(self, request, *args, **kwargs):
        # 로그인 기능이 없기 때문에 막아둔다.
        pass

    def put(self, *args, **kwargs):
        # 로그인 기능이 없기 때문에 막아둔다.
        pass
