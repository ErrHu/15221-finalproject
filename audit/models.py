from django.contrib.auth.models import User
from django.db import models


class UserAudit(models.Model):
    user = models.OneToOneField(User, null=False, blank=False)
    audit = models.TextField(null=False, default="")
