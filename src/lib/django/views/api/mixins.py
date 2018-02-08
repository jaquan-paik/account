import math
from typing import Dict, Tuple

from django.core.paginator import Paginator
from django.utils.http import http_date
from rest_framework.response import Response

from infra.network.constants.api_status_code import ApiStatusCodes, StatusCode
from infra.network.constants.custom_header import CustomHttpHeader
from lib.base.exceptions import ErrorException
from .dto import LastModified, ResponseCode

DEFAULT_ITEMS_PER_PAGE = 40


class PaginateMixin:
    @staticmethod
    def paginate(items, page: int, item_count_per_page: int) -> Tuple:
        """
        deprecated
        django 의존성을 최소화하기 위해서 django Paginator 를 사용하지 않는 쪽으로 변경 필요
        """
        if page is None or not isinstance(page, int):
            page = 1

        paginator = Paginator(items, item_count_per_page)
        total_items = paginator.count
        total_pages = paginator.num_pages
        paginated_items = paginator.page(page)

        return paginated_items, total_items, total_pages, page

    @staticmethod
    def get_page_info(cur_page: int, items_per_page: int) -> Tuple:
        cur_pos = (cur_page - 1) * items_per_page
        return cur_page, items_per_page, cur_pos

    @staticmethod
    def get_pagination(total_count: int, cur_page: int, items_per_page: int=DEFAULT_ITEMS_PER_PAGE) -> Dict:
        if cur_page is None or not isinstance(cur_page, int):
            cur_page = 1

        total_page = 1
        if total_count != 0:
            total_page = math.ceil(total_count / items_per_page)

        return {
            'cur_page': cur_page,
            'total_count': total_count,
            'total_page': total_page,
        }

    @staticmethod
    def get_offset_pagination(total_count: int, cur_offset: int, limit: int) -> Dict:
        return {
            'offset': cur_offset,
            'total_count': total_count,
            'limit': limit,
        }


class VersioningMixin:
    def get(self, request, *args, **kwargs):
        return self._route_api('get', request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self._route_api('post', request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self._route_api('put', request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self._route_api('delete', request, *args, **kwargs)

    def _route_api(self, method_name: str, request, *args, **kwargs):
        version = request.META.get(CustomHttpHeader.API_VERSION_HEADER) or '1'
        method_name_with_version = '{}_v{}'.format(method_name, version)

        if hasattr(self, method_name_with_version) is False:
            method_name_with_version = '{}_v1'.format(method_name)

        return getattr(self, method_name_with_version)(request, *args, **kwargs)


class ResponseMixin:
    def _make_response(self, response_code: ResponseCode, data=None, last_modified: LastModified=None) -> Response:
        if data is None:
            data = {}

        if 'message' in data or 'code' in data:
            raise ErrorException('데이터 필드명 중 예약어가 포함되어 있습니다.')

        if response_code.has_message():
            data['message'] = response_code.get_message()
        if response_code.has_code():
            data['code'] = response_code.get_code()

        headers = {}
        if last_modified is None:
            last_modified = LastModified()
        if last_modified.last_modified is not None:
            headers['Last-Modified'] = http_date(last_modified)
        if last_modified.e_tag is not None:
            headers['ETag'] = '"{}"'.format(last_modified.e_tag)

        return Response(data, status=response_code.get_status(), headers=headers)

    def make_response_code(self, status: StatusCode, msg: str=None) -> ResponseCode:
        return ResponseCode(status_code=status, message=msg)

    def make_last_modified(self, last_modified: int=None, e_tag: str=None) -> LastModified:
        return LastModified(last_modified=last_modified, e_tag=e_tag)

    def success_response(self, data=None, response_code: ResponseCode=None, last_modified: LastModified=None) -> Response:
        if response_code is None:
            response_code = ResponseCode(ApiStatusCodes.C_200_OK)
        return self._make_response(response_code, data=data, last_modified=last_modified)

    def fail_response(self, response_code: ResponseCode, data=None) -> Response:
        return self._make_response(response_code, data=data)
