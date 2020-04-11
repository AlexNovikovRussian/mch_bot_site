from django.db import models
from django.conf import settings

# Create your models here.

class MosUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_constraint=False, null=True, blank=True, default="00")
    mosLogin = models.CharField(max_length=50, verbose_name="Mos.ru login")
    mosPassword = models.CharField(max_length=50, verbose_name="Mos.ru password")

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = 'Mos.ru user'
        verbose_name_plural = 'Mos.ru users'
    