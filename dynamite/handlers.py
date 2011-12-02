from django.contrib.auth.management import create_permissions
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import get_app
from dynamite import db, signals, registry

def attribute_pre_save(sender, instance, **kwargs):
    try:
        instance._old_slug = sender.objects.filter(pk=instance.pk).exclude(slug=instance.slug).get().slug
    except ObjectDoesNotExist:
        pass

def attribute_post_save(sender, instance, created, **kwargs):
    entity = instance.schema.get_entity(regenerate = True)
    if hasattr(instance, '_old_slug'):
        db.rename_column(entity, instance._old_slug, instance.slug)
        del instance._old_slug
    db.add_necessary_columns(entity)
    registry.cache.set(entity._meta.app_label, entity._meta.object_name)
    signals.dynamic_model_changed.send(sender, entity=entity)

def attribute_pre_delete(sender, instance, **kwargs):
    old_fields = [f.name for f in instance.schema.entity._meta.local_fields]
    setattr(instance, '_old_fields', old_fields)

def attribute_post_delete(sender, instance, **kwargs):
    entity = instance.schema.get_entity(regenerate = True)
    if hasattr(instance, '_old_fields'):
        db.delete_unnecessary_columns(entity, instance._old_fields)
        del instance._old_fields
    registry.cache.set(entity._meta.app_label, entity._meta.object_name)
    signals.dynamic_model_changed.send(sender, entity=entity)

def schema_post_save(sender, instance, created, **kwargs):
    entity = instance.get_entity(regenerate = True)
    db.create_table(entity)
    registry.cache.set(entity._meta.app_label, entity._meta.object_name)
    create_permissions(get_app(entity._meta.app_label), created_models=[], verbosity=0)
    signals.dynamic_model_changed.send(sender, entity=entity)

def schema_post_delete(sender, instance, **kwargs):
    entity = instance.get_entity()
    ContentType.objects.get_for_model(entity).delete()
    ContentType.objects.clear_cache()
    registry.cache.delete(entity._meta.app_label, entity._meta.object_name)
    db.delete_table(entity)
    signals.dynamic_model_deleted.send(sender, entity=entity)
