import urllib.parse


def generate_query_url(url: str, params: dict):
    url_parts = list(urllib.parse.urlparse(url))
    query = dict(urllib.parse.parse_qsl(url_parts[4]))
    query.update(params)

    url_parts[4] = urllib.parse.urlencode(query)

    return urllib.parse.urlunparse(url_parts)


# TODO: query key value 비교로 후에 변경
def get_url_until_path(url: str):
    split_url = urllib.parse.urlsplit(url)
    return f"{split_url[0]}/{split_url[1]}{split_url[2]}"
