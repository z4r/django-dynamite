from contextlib import contextmanager
from south.db import db
from django.db import connection

@contextmanager
def south_transaction():
    db.start_transaction()
    try:
        yield db
    except Exception:
        db.rollback_transaction()
    else:
        db.commit_transaction()

def create_table(entity):
    table_name = entity._meta.db_table
    if not table_exist(table_name):
        fields = [(f.name, f) for f in entity._meta.local_fields]
        with south_transaction() as db:
            db.create_table(table_name, fields)
            db.execute_deferred_sql()

def delete_table(entity):
    with south_transaction() as db:
        db.delete_table(entity._meta.db_table)

def add_necessary_columns(entity):
    create_table(entity)
    table_name = entity._meta.db_table
    db_column_names = get_column_names(table_name)
    with south_transaction() as db:
        for field in entity._meta.local_fields:
            if field.column not in db_column_names:
                db.add_column(table_name, field.name, field)
        db.execute_deferred_sql()

def delete_unnecessary_columns(entity, old_fields):
    table_name = entity._meta.db_table
    if table_exist(table_name):
        new_fields = [f.name for f in entity._meta.local_fields]
        with south_transaction() as db:
            for field_name in old_fields:
                if field_name not in new_fields:
                    db.delete_column(table_name, field_name)

def rename_column(entity, old_name, new_name):
    with south_transaction() as db:
        db.rename_column(entity._meta.db_table, old_name, new_name)

def table_exist(table_name):
    ci = connection.introspection
    return ci.table_name_converter(table_name) in ci.table_names()

def get_column_names(table_name):
    ci = connection.introspection
    cursor = connection.cursor()
    return [row[0] for row in ci.get_table_description(cursor, table_name)]
