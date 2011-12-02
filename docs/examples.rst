Examples
========

Survey System
=============

*survey.models.py*

::

    from django.db import models
    from dynamite.models import AbstractSchema, AbstractAttribute, AbstractEntity
    from dynamite.registry import register

    class Survey(AbstractSchema):
        class Meta:
            verbose_name = 'survey'
            verbose_name_plural = 'surveys'

    class Question(AbstractAttribute):
        rank = models.PositiveIntegerField(default=5)
        schema = models.ForeignKey(Survey)

        class Meta:
            ordering = ['rank']
            verbose_name = 'question'
            verbose_name_plural = 'questions'

    class Response(AbstractEntity):
        class Meta:
            abstract = True
            verbose_name = 'response'
            verbose_name_plural = 'responses'

    register(
        schema = Survey,
        attribute = Question,
        entity = Response,
    )

*survey.models.py*

::

    from django.contrib import admin
    from dynamite.admin import register
    from survey.models import Survey

    register(Survey)

ContentType and generic
=======================

*skill.models.py*

::

    from django.contrib.contenttypes.models import ContentType
    from django.db.models.signals import post_save
    from django.contrib.contenttypes import generic
    from django.db import models
    from django.utils.translation import ugettext_lazy as _
    from dynamite.models import AbstractSchema, AbstractEntity
    from dynamite.registry import register

    class Worker(models.Model):
        cf = models.CharField(max_length = 16, primary_key = True)
        content_type = models.ForeignKey(ContentType)
        object_id = models.IntegerField()
        content_object = generic.GenericForeignKey('content_type', 'object_id')

        def __unicode__(self):
            return self.cf

        class Meta:
            ordering = ('cf',)
            unique_together = ('content_type', 'object_id')
            verbose_name = _('worker')
            verbose_name_plural = _('workers')

    class SkilledWorker(AbstractEntity):
        cf = models.CharField(max_length = 16)
        item = generic.GenericRelation(Worker)

        class Meta:
            abstract = True

        def __unicode__(self):
            return self.cf

        class Meta:
            verbose_name = _('skilled worker')
            verbose_name_plural = _('skilled workers')

    def update_item(instance, raw, created, **kwargs):
        if isinstance(instance, SkilledWorker):
            if created:
                item = Worker()
                item.cf = instance.cf
                item.content_type = ContentType.objects.get_for_model(type(instance))
                item.object_id = instance.id
            else:
                item = instance.item.all()[0]
            item.save()

    post_save.connect(update_item)

    class SkillGroup(AbstractSchema):
        class Meta:
            verbose_name = _('skill group')
            verbose_name_plural = _('skill groups')

    register(
        schema = SkillGroup,
        entity = SkilledWorker,
    )

*skill.admin.py*

::

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
