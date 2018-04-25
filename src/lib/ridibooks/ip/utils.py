from lib.ridibooks.ip.constants import RidiIP
from lib.utils.ip import get_client_ip_from_request, is_internal_ip


def is_ridi_ip_from_request(request) -> bool:
    client_ip = get_client_ip_from_request(request)
    return is_internal_ip(client_ip) or RidiIP.is_ridi_ip(client_ip)
