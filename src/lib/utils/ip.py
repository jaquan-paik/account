import ipaddress

import iptools
from ipware.ip import get_ip


def is_ipv6(ip: str) -> bool:
    return ':' in ip


def ip2long(ip: str) -> int:
    if is_ipv6(ip):
        return iptools.ipv6.ip2long(ip)

    return iptools.ipv4.ip2long(ip)


def long2ip(ip: int) -> str:
    if ip > iptools.ipv4.MAX_IP:
        return iptools.ipv6.long2ip(ip)

    return iptools.ipv4.long2ip(ip)


def get_client_ip_from_request(request) -> str:
    return get_ip(request)


def is_internal_ip(ip: str) -> bool:
    return ipaddress.ip_address(ip).is_private
