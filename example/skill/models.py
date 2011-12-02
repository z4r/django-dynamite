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