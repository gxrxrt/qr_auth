from django.db import models

class CustomUser(models.Model):
    login = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    status = models.BooleanField(default=False)  # True - доступ, False - ошибка

    def __str__(self):
        return self.login
