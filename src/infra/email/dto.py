class Email:
    def __init__(self, email: str, name: str=None):
        self.email = email
        self.name = name

    def __str__(self):
        if self.has_name():
            return '{} <{}>'.format(self.name, self.email)

        return self.email

    def has_name(self) -> bool:
        return self.name is not None
