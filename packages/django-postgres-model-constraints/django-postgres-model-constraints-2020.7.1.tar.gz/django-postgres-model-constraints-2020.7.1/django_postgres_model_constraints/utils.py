import hashlib
from django.apps import apps
from django.db import models


def getmd5(string):
    m = hashlib.md5()
    m.update(string.encode('utf-8'))
    return m.hexdigest()


DJANGO_APP_LABELS = [
    'admin',
    'auth',
    'contenttypes',
    'django',
    'sessions',
    'sites'
]


ON_DELETE = {
    models.CASCADE: 'CASCADE',
    models.SET_NULL: 'SET NULL',
    models.PROTECT: 'RESTRICT',
    models.DO_NOTHING: 'NO ACTION'
}


def get_models(self):
    models = []
    for model in apps.get_models():
        if model._meta.app_label not in DJANGO_APP_LABELS:
            models.append(model._meta.app_label)
    return models


def get_unique_fields(model):
    return list(filter(lambda f: f.unique and not f.primary_key, model._meta.fields))


def get_foreign_key_fields(model):
    return list(filter(lambda f: f.remote_field, model._meta.fields))


def get_unique_constraint_name(f):
    return '%s_%s_key' % (f.model._meta.db_table, f.name)


def get_foreign_key_constraint_name(f):
    return '%s_fk_%s_id' % (f.attname, f.remote_field.model._meta.db_table)


def get_unique_together_constraint_name(model, unique_together):
    conname = '%s_%s_uniq' % (model._meta.db_table, '_'.join(unique_together))
    if len(conname) > 63:
        return '%s_%s_uniq' % (model._meta.db_table, getmd5(','.join(unique_together)))
    return conname


def get_unique_together(model):
    if not any(isinstance(el, (list, tuple)) for el in model._meta.unique_together):
        return [model._meta.unique_together]
    return model._meta.unique_together


def get_add_unique_constraint_statement(f):
    return """
ALTER TABLE %s
ADD CONSTRAINT %s UNIQUE (%s);
    """ % (f.model._meta.db_table, get_unique_constraint_name(f), f.attname)


def get_drop_unique_constraint_statement(f):
    return """
ALTER TABLE %s
DROP CONSTRAINT %s;
    """ % (f.model._meta.db_table, get_unique_constraint_name(f))


def get_add_unique_together_constraint_statements(model):
    statements = []
    for unique_together in get_unique_together(model):
        if not unique_together:
            continue
        attnames = list(map(
            lambda f: model._meta.get_field(f).attname, unique_together
        ))
        name = get_unique_together_constraint_name(model, unique_together)
        sql = """
ALTER TABLE %s
ADD CONSTRAINT %s UNIQUE (%s);
        """ % (model._meta.db_table, name, ','.join(attnames))
        statements.append(sql.strip())
    return statements


def get_drop_unique_together_constraint_statements(model):
    statements = []
    for unique_together in get_unique_together(model):
        if not unique_together:
            continue
        name = get_unique_together_constraint_name(model, unique_together)
        s = "ALTER TABLE %s DROP CONSTRAINT %s;" % (
            model._meta.db_table, name)
        statements.append(s.strip())
    return statements


def get_add_unique_constraint_statements(model):
    statements = []
    for f in filter(lambda f: f.unique and not f.primary_key, model._meta.fields):
        statements.append(get_add_unique_constraint_statement(f).strip())
    return statements + get_add_unique_together_constraint_statements(model)


def get_drop_unique_constraint_statements(model):
    statements = []
    for f in get_unique_fields(model):
        statements.append(get_drop_unique_constraint_statement(f).strip())
    return statements + get_drop_unique_together_constraint_statements(model)


def get_add_foreign_key_constraint_statements(model):
    statements = []
    for f in get_foreign_key_fields(model):
        name = get_foreign_key_constraint_name(f)
        on_delete = ON_DELETE[f.remote_field.on_delete]
        sql = """
ALTER TABLE %s
ADD CONSTRAINT %s
FOREIGN KEY (%s) REFERENCES %s(id) ON DELETE %s DEFERRABLE INITIALLY DEFERRED;""" % (model._meta.db_table, name, f.attname, f.remote_field.model._meta.db_table, on_delete)
        statements.append(sql.strip())
    return statements


def get_drop_foreign_key_constraint_statements(model):
    statements = []
    for f in get_foreign_key_fields(model):
        name = get_foreign_key_constraint_name(f)
        s = "ALTER TABLE %s DROP CONSTRAINT %s;" % (model._meta.db_table, name)
        statements.append(s)
    return statements
