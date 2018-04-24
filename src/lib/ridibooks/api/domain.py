from infra.configure.config import GeneralConfig


class ApiDomain:
    def __init__(self, dev, prod):
        self.dev = dev
        self.prod = prod

    def __get__(self, instance, owner):
        if GeneralConfig.is_dev():
            return self.dev

        return self.prod
