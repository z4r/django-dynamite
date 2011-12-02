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