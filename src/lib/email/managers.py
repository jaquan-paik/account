from django.db import models


class EmailBlacklistManager(models.Manager):
    def is_in_blacklist(self, email: str) -> bool:
        return self.filter(email=email, is_active=True).count() > 0
