from django.db import models
from django.db.models import signals
from dynamite import fields, handlers, registry

class AbstractSchema(models.Model):
    """This abstract model represents the Tables container (As a Database).

You should inherit from this class when you want to start a dynamical model system.

::

    from dynamite.models import AbstractSchema
    from dynamite.registry import register

    class Survey(AbstractSchema):
        class Meta:
            verbose_name = 'survey'
            verbose_name_plural = 'surveys'

.. note::
    To activate this schema remember to register it in `yourapp.models` with:

::

    register(
        schema = Survey,
    )
    """
    name = models.CharField(max_length = 255)
    slug = models.SlugField(unique = True)

    _super_entity = NotImplemented
    _attribute = NotImplemented

    class Meta:
        abstract = True
        ordering = ('name',)

    def __unicode__(self):
        return self.name

    @classmethod
    def bind(cls, entity_cls, attribute_cls):
        cls._super_entity = entity_cls or AbstractEntity
        cls._attribute = attribute_cls or AbstractAttribute.factory(cls)
        cls._attribute._meta.unique_together = list(cls._attribute._meta.unique_together)
        cls._meta.ordering = cls._meta.ordering or AbstractSchema.Meta.ordering
        for ut in AbstractAttribute.Meta.unique_together:
            if ut not in cls._attribute._meta.unique_together:
                cls._attribute._meta.unique_together.append(ut)
        signals.pre_save.connect(
            handlers.attribute_pre_save, sender=cls._attribute
        )
        signals.post_save.connect(
            handlers.attribute_post_save, sender=cls._attribute
        )
        signals.pre_delete.connect(
            handlers.attribute_pre_delete, sender=cls._attribute
        )
        signals.post_delete.connect(
            handlers.attribute_post_delete, sender=cls._attribute
        )
        signals.post_save.connect(
            handlers.schema_post_save, sender=cls
        )
        signals.post_delete.connect(
            handlers.schema_post_delete, sender=cls
        )

    @property
    def entity(self):
        return self.get_entity()

    def get_entity(self, regenerate=False):
        name = self.slug.replace('-', '_').encode('ascii', 'ignore')
        app_name = self._super_entity._meta.app_label
        model_name = self._super_entity.__name__ + '_' +name

        cached_model = registry.cache.get(app_name, model_name, regenerate)
        if cached_model is not None:
            return cached_model

        attrs = {
            '__module__': getattr(self._super_entity, '__module__',  __name__),
        }

        class Meta:
            app_label = app_name
            verbose_name = self.name.lower() + ' ' + unicode(self._super_entity._meta.verbose_name)
        attrs['Meta'] = Meta

        for attribute in getattr(self, self._attribute._meta.get_field('schema').related.get_accessor_name()).all():
            field_name = attribute.slug.replace('-','_').encode('ascii', 'ignore')
            attrs[field_name] = attribute.get_field()

        model = type(model_name, (self._super_entity,), attrs)
        return model

class AbstractAttribute(models.Model):
    """This abstract model represents the table's fields template.

You should inherit from this class when you want to add something to this template.

::

    from django.db import models
    from dynamite.models import AbstractSchema, AbstractAttribute
    from dynamite.registry import register

    class Survey(AbstractSchema):
        class Meta:
            verbose_name = 'survey'
            verbose_name_plural = 'surveys'

.. note::
    You have to make a foreign key through the schema:

::

    class Question(AbstractAttribute):
        rank = models.PositiveIntegerField(default=5)
        schema = models.ForeignKey(Survey)

        class Meta:
            ordering = ['rank']
            verbose_name = 'question'
            verbose_name_plural = 'questions'

.. note::
    To activate this schema remember to register it in `yourapp.models` with:

::

    register(
        schema = Survey,
        attribute = Question,
    )

.. note::
    At the moment an Attribute can be:
        * Short text
        * Long text
        * Number
        * Decimal number
    """
    schema      = NotImplemented
    name        = models.CharField(max_length=255, default="")
    slug        = models.SlugField()
    attr_type   = models.CharField(max_length=32, choices=fields.ATTR_TYPES)
    choices     = models.CharField(max_length=1024, default="", blank=True,
                    help_text="comma separated choices, keep them shortish")
    required    = models.BooleanField(default=False)

    def get_field(self):
        kwargs = {
            'blank' : not self.required,
            'verbose_name' : self.name,
        }
        if self.choices.strip():
            kwargs['choices'] = [(x.strip(), x.strip()) for x in self.choices.split(",")]

        try:
            return fields.ATTR_FIELDS[self.attr_type](**kwargs)
        except KeyError:
            return None

    class Meta:
        abstract = True
        unique_together =  (('schema', 'slug'),)

    @classmethod
    def factory(cls, schema):
        return type(
            'Attribute',
            (cls,),
            dict(
                schema = models.ForeignKey(schema),
                __module__ = getattr(schema, '__module__'),
            )
        )

class AbstractEntity(models.Model):
    """This abstract model represents the Table.

You should inherit from this class when you want something in common in your schema.
For example you want share uniqueness of primary keys

::

    from django.db import models
    from dynamite.models import AbstractSchema, AbstractEntity
    from dynamite.registry import register

    class Survey(AbstractSchema):
        class Meta:
            verbose_name = 'survey'
            verbose_name_plural = 'surveys'

    class Response(AbstractEntity):
        name = models.CharFields(primary_key = True)
        class Meta:
            abstract = True
            verbose_name = 'response'
            verbose_name_plural = 'responses'

.. note::
    To activate this schema remember to register it in `yourapp.models` with:

::

    register(
        schema = Survey,
        entity = Response,
    )
    """
    class Meta:
        abstract = True
