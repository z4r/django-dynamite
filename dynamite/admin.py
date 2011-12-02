from django.contrib import admin
from django.core.urlresolvers import clear_url_caches
from django.utils.importlib import import_module
from django.conf import settings
from dynamite import signals

def register(schema):
    """ This method allow to register a SchemaAttributeEntity pattern in the
    django admin interface

::

    from dynamite.admin import register
    from survey.models import Survey

    register(Survey)
    """
    class SchemaAdmin(admin.ModelAdmin):
        list_display = ('name', 'slug')
        prepopulated_fields = {'slug' : ('name',)}
        inlines = [
            type(
                'AttributeInline',
                (admin.TabularInline, ),
                dict(
                    model = schema._attribute,
                    prepopulated_fields = {'slug' : ('name',)},
                )
            )
        ]
    admin.site.register(schema, SchemaAdmin)
    for s in schema.objects.all():
        reregister(s, s.entity)
    signals.dynamic_model_changed.connect(reregister)
    signals.dynamic_model_deleted.connect(unregister)

def reregister(sender, entity, **kwargs):
    unregister(sender, entity)
    admin.site.register(entity, admin_list_factory(entity))
    reload(import_module(settings.ROOT_URLCONF))
    clear_url_caches()

def unregister(sender, entity, **kwargs):
    for reg_model in admin.site._registry.keys():
        if entity._meta.db_table == reg_model._meta.db_table:
            del admin.site._registry[reg_model]
    try:
        admin.site.unregister(entity)
    except admin.sites.NotRegistered:
        pass
    reload(import_module(settings.ROOT_URLCONF))
    clear_url_caches()

def admin_list_factory(model):
    fields = [f.name for f in model._meta.fields if not f.auto_created]
    return type('EntityAdmin', (admin.ModelAdmin,), {'list_display' : fields,})
