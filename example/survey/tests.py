from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from models import Survey

class SurveyTestCase(TestCase):
    def test_basic(self):
        instance = Survey.objects.get(name='Personal Data')
        qs = [e for e in instance.entity.objects.all()]
        self.assertEqual(len(qs), 1)
        johndoe = qs.pop()
        self.assertEqual(johndoe.first_name,  'John')
        self.assertEqual(johndoe.last_name,  'Doe')
        self.assertEqual(johndoe.age,  31)

    def test_remove_add_age(self):
        age = Survey._attribute.objects.get(name='Age')
        age.delete()
        instance = Survey.objects.get(name='Personal Data')
        qs = [e for e in instance.entity.objects.all()]
        self.assertEqual(len(qs), 1)
        johndoe = qs.pop()
        self.assertEqual(johndoe.first_name,  'John')
        self.assertEqual(johndoe.last_name,  'Doe')
        self.assertRaises(AttributeError, getattr, johndoe, 'age')
        Survey._attribute.objects.create(
            name = 'Age',
            slug = 'age',
            attr_type = 'Integer',
            schema = instance,
        )
        qs = [e for e in instance.entity.objects.all()]
        self.assertEqual(len(qs), 1)
        johndoe = qs.pop()
        self.assertEqual(johndoe.first_name,  'John')
        self.assertEqual(johndoe.last_name,  'Doe')
        self.assertEqual(johndoe.age,  None)
        johndoe.age = 31
        johndoe.save()
        qs = [e for e in instance.entity.objects.all()]
        self.assertEqual(len(qs), 1)
        johndoe = qs.pop()
        self.assertEqual(johndoe.first_name,  'John')
        self.assertEqual(johndoe.last_name,  'Doe')
        self.assertEqual(johndoe.age,  31)

    def test_remove_add_rename_model(self):
        instance = Survey.objects.get(name='Personal Data')
        entity = instance.entity
        app_label = entity._meta.app_label
        object_name = entity._meta.object_name.lower()
        ctype = ContentType.objects.get(app_label=app_label, model=object_name)
        perms = Permission.objects.filter(content_type=ctype)
        self.assertEqual(len(perms), 3)
        instance.delete()
        self.assertRaises(ObjectDoesNotExist, ContentType.objects.get, app_label=app_label, model=object_name)
        perms = Permission.objects.filter(content_type=ctype)
        self.assertEqual(len(perms), 0)
        instance = Survey.objects.create(name='Personal Data', slug='personal-data')
        Survey._attribute.objects.get_or_create(
            name = 'First Name',
            slug = 'first-name',
            attr_type = 'ShortText',
            schema = instance,
            required = True,
        )
        Survey._attribute.objects.get_or_create(
            name = 'Last Name',
            slug = 'last-name',
            attr_type = 'ShortText',
            schema = instance,
            required = True,
        )
        Survey._attribute.objects.get_or_create(
            name = 'Age',
            slug = 'age',
            attr_type = 'Integer',
            schema = instance,
        )
        Survey._attribute.objects.get_or_create(
            name = 'Age',
            slug = 'age',
            attr_type = 'Integer',
            schema = instance,
        )
        self.assertEqual(len(Survey._attribute.objects.all()), 3)
        entity = instance.entity
        app_label = entity._meta.app_label
        object_name = entity._meta.object_name.lower()
        ctype = ContentType.objects.get(app_label=app_label, model=object_name)
        perms = Permission.objects.filter(content_type=ctype)
        self.assertEqual(len(perms), 3)
        johndoe = instance.entity.objects.create(
            first_name = 'John',
            last_name = 'Doe',
            age =  31,
        )
        self.assertEqual(johndoe.first_name,  'John')
        self.assertEqual(johndoe.last_name,  'Doe')
        self.assertEqual(johndoe.age,  31)
        age = Survey._attribute.objects.get(name='Age')
        age.name = 'Eta'
        age.slug = 'eta'
        age.save()
        instance = Survey.objects.get(name='Personal Data')
        qs = [e for e in instance.entity.objects.all()]
        self.assertEqual(len(qs), 1)
        johndoe = qs.pop()
        self.assertEqual(johndoe.first_name,  'John')
        self.assertEqual(johndoe.last_name,  'Doe')
        self.assertRaises(AttributeError, getattr, johndoe, 'age')
        self.assertEqual(johndoe.eta,  31)
        age.name = 'Age'
        age.slug = 'age'
        age.save()
        self.assertEqual(len(Survey._attribute.objects.all()), 3)