from lib.base.exceptions import MsgException


def assert_allowed_hosts_with_cookie_root_domain(allowed_hosts: [], cookie_root_domain: str) -> None:
    for host in allowed_hosts:
        if not host[::-1].find(cookie_root_domain[::-1]) == 0:  # host의 끝이 cookie_rood_domain으로 끝나는지 확인한다.
            raise MsgException(f"{host}의 root domain이 {cookie_root_domain}가 아닙니다.")
