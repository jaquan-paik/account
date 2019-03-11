from urllib import parse

SCHEME = 0
NETLOC = 1
PATH = 2
QUERY = 3
FRAGMENT = 4


def generate_query_url(url: str, params: dict):
    url_parts = list(parse.urlsplit(url))  # list로 묶지 않으면 query를 업데이트 할 수가 없음.
    query = dict(parse.parse_qsl(url_parts[QUERY]))
    query.update(params)

    url_parts[QUERY] = parse.urlencode(query)

    return parse.urlunsplit(url_parts)


def get_url_until_path(url: str):
    split_url = parse.urlsplit(url)
    return f"{split_url[SCHEME]}/{split_url[NETLOC]}{split_url[PATH]}"


def is_url(url: str) -> bool:
    parsed_url = parse.urlsplit(url)
    return parsed_url[SCHEME] and parsed_url[NETLOC]


def is_same_path(first_path: str, second_path: str) -> bool:
    if first_path == second_path:
        return True

    if first_path and first_path[-1] == '/' and first_path[:-1] == second_path:
        return True

    if second_path and second_path[-1] == '/' and second_path[:-1] == first_path:
        return True

    return False


def is_same_query(first_query: dict, second_query: dict) -> bool:
    first_query_keys = first_query.keys()
    second_query_keys = second_query.keys()

    if not first_query_keys == second_query_keys:
        return False

    for key in first_query_keys:
        first_value = first_query.get(key)
        second_value = second_query.get(key)

        if is_url(first_value):  # query 안에 url 이 있는 경우, url 비교로 넘어간다.
            result = is_same_url(first_value, second_value)

        else:
            result = first_value == second_value

        if not result:
            return False

    return True


def is_same_url(first_url: str, second_url: str) -> bool:
    if not is_url(first_url) or not is_url(second_url):
        return False

    first_parsed_url = parse.urlsplit(first_url)
    second_parsed_url = parse.urlsplit(second_url)

    if not first_parsed_url[:PATH] == second_parsed_url[:PATH]:
        return False
    if not is_same_path(first_parsed_url[PATH], second_parsed_url[PATH]):
        return False

    if not first_parsed_url[FRAGMENT] == second_parsed_url[FRAGMENT]:
        return False

    first_url_query = dict(parse.parse_qsl(first_parsed_url[QUERY]))
    second_url_query = dict(parse.parse_qsl(second_parsed_url[QUERY]))
    if not is_same_query(first_url_query, second_url_query):
        return False

    return True


def is_same_url_until_path(first_url: str, second_url: str) -> bool:
    if not is_url(first_url) or not is_url(second_url):
        return False

    first_parsed_url = parse.urlsplit(first_url)
    second_parsed_url = parse.urlsplit(second_url)

    if not first_parsed_url[:PATH] == second_parsed_url[:PATH]:
        return False

    if not is_same_path(first_parsed_url[PATH], second_parsed_url[PATH]):
        return False

    return True
