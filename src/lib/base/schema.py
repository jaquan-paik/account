from typing import Dict, List, Optional, Union

from drf_yasg.openapi import Parameter, Response, Schema, SchemaRef
from rest_framework.serializers import Serializer

REQUEST_BODY = Union[Schema, SchemaRef, Serializer]
QUERY_SERIALIZER = Optional[Serializer]
MANUAL_PARAMETERS = List[Parameter]
RESPONSES = Dict[str, Union[Schema, SchemaRef, Response, str, Serializer]]


class BaseSchema:
    """
    https://github.com/axnsan12/drf-yasg

    ### Description ###

    -> GET의 경우
    request_body가 동작하지 않는다.
    query_serializer에 serializer를 지정하던가
    혹은 manual_parameters에 Parameter객체들을 만들어서 list로 만들어 지정해준다.

    -> POST, PUT, PATCH의 경우
    request_body에 데이터를 셋팅한다. Serializer 혹은 Schema 객체를 생성해서 지정해주면된다.

    -> Responses Dictionary로 구성되어있고
    key는 Status Code
    value는 Schema 혹은 Response 혹은 Serializer 혹은 string 이다.

    -> 위의 데이터들에서 Serializer를 받는 변수들은 내부에서 자동으로 `serializer_to_schema`를 통해 변환해준다.

    #### Type Hint ####

    :type request_body: REQUEST_BODY
    :type query_serializer: QUERY_SERIALIZER
    :type manual_parameters: MANUAL_PARAMETERS
    :type responses: RESPONSES
    """
    request_body = None
    query_serializer = None
    manual_parameters = None
    responses = None

    @classmethod
    def to_swagger_schema(cls) -> Dict:
        _schema = {}

        if cls.request_body:
            _schema['request_body'] = cls.request_body
        if cls.query_serializer:
            _schema['query_serializer'] = cls.query_serializer
        if cls.manual_parameters:
            _schema['manual_parameters'] = cls.manual_parameters
        if cls.responses:
            _schema['responses'] = cls.responses

        return _schema
