from django.db import models
from dynamite import db

class DymoSite(object):
    def __init__(self):
        self._registry = set()
        self._cache = set()

    def register(self, schema, entity=None, attribute=None):
        schema.bind(entity, attribute)
        self._registry.add(schema)
        if db.table_exist(schema._meta.db_table):
            for s in schema.objects.all():
                s.get_entity(regenerate=True)

    def iter_models(self, *schemas):
        schemas = schemas or self._registry
        for schema in schemas:
            for s in schema.objects.all():
                db.add_necessary_columns(s.entity)
                yield s.entity

    def get_models(self, *schemas):
        return set(self.iter_models(*schemas))


class DymoCache(object):
    def __init__(self):
        self._cache = set()

    def get(self, app_label, model_name, regenerate=False):
        model = models.get_model(app_label, model_name)
        if regenerate or model and (app_label, model_name) not in self._cache:
            model = None
            self.delete(app_label, model_name)
        return model

    def set(self, app_label, model_name):
        self._cache.add((app_label, model_name))

    def delete(self, app_label, model_name):
        try:
            del models.loading.cache.app_models[app_label][model_name.lower()]
        except KeyError:
            pass
        self._cache.discard((app_label, model_name))

site = DymoSite()
cache = DymoCache()

def register(schema, entity=None, attribute=None):
    site.register(schema, entity, attribute)
