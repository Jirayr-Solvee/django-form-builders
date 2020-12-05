# Django imports
from django.db import models
from django.core.serializers.json import DjangoJSONEncoder

# Project imports
import json


class JSONField(models.TextField):
    """
    JSONField is a TextField which serialize/deserialize JSON objects.

    Example:
        class Book(models.Model):
            data = JSONField(blank=True, null=True)

        book = Book.objects.get(pk=5)
        book.data = {'title': 'test', 'price': 3}
        book.save()
    """

    def to_python(self, value):
        if value == "":
            return None

        try:
            if isinstance(value, str):
                return json.loads(value)
        except ValueError:
            pass
        return value

    def from_db_value(self, value, *args):
        return self.to_python(value)

    def get_db_prep_save(self, value, *args, **kwargs):
        if value == "":
            return None
        if isinstance(value, dict):
            value = json.dumps(value, cls=DjangoJSONEncoder)
        return value


class CreatedForms(models.Model):
    name = models.CharField(max_length=250)
    fields = JSONField(blank=True, null=True)

    class Meta:
        verbose_name = ("Created Form")
        verbose_name_plural = ("Created Forms")

    def __str__(self):
        return self.name


class SubmittedForms(models.Model):
    form = models.ForeignKey(CreatedForms, on_delete=models.CASCADE)
    data = JSONField(blank=True, null=True)

    class Meta:
        verbose_name = ("Submitted Form")
        verbose_name_plural = ("Submitted Forms")
