from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from dynamite.admin import register

from survey.models import Survey


register(Survey)

admin.site.register(ContentType)
admin.site.register(Permission)
