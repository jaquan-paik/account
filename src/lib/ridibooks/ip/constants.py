from lib.base.constants import BaseConstant


class RidiIP(BaseConstant):
    OFFICE_01 = '218.232.41.2'
    OFFICE_04 = '218.232.41.5'

    VPN_01 = '222.231.4.165'
    VPN_02 = '222.231.4.164'

    IDC_01 = '115.68.53.154'

    _LIST = (OFFICE_01, OFFICE_04, VPN_01, VPN_02, IDC_01, )

    _STRING_MAP = {
        OFFICE_01: '어반벤치 01',
        OFFICE_04: '어반벤치 04',

        VPN_01: 'VPN 01',
        VPN_02: 'VPN 02',

        IDC_01: 'IDC 01',
    }

    @classmethod
    def is_ridi_ip(cls, ip: str) -> bool:
        for ridi_ip in cls.get_list():
            if ip == ridi_ip:
                return True
        return False
