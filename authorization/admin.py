from django.contrib import admin
from django.contrib.admin import ModelAdmin

from authorization.models import CustomUser


admin.site.register(CustomUser)