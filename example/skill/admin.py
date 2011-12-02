from django.contrib import admin
from skill.models import Worker, SkillGroup
from dynamite.admin import register

class WorkerAdmin(admin.ModelAdmin):
    search_fields = ['cf']
    list_display = ['link_to_content', 'content_type']

    def link_to_content(self, item):
        target = getattr(item, 'content_object')
        return u'<a href="../../%s/%s/%s">%s</a>' % (
            target._meta.app_label,
            target._meta.module_name,
            target.pk,
            target
        )
    link_to_content.__name__ = 'CF'
    link_to_content.allow_tags = True
    link_to_content.admin_order_field = 'cf'

admin.site.register(Worker, WorkerAdmin)
register(SkillGroup)
