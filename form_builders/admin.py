# Django imports
from django.contrib import admin
from django.forms import widgets
from django import forms

# Project imports
from . import models


class SubmittedForm(forms.ModelForm):
    class Meta:
        model = models.SubmittedForms
        exclude = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.initial:
            created_fields = models.CreatedForms.objects.get(pk=self.initial['form']).fields
            for x, y in eval(self.initial['data']).items():
                for field in eval(created_fields):
                    if field['label'] == x:
                        label = field['type'].split('-')[0]
                        if label == 'textarea':
                            self.base_fields[x] = forms.CharField(
                                initial=y, widget=forms.Textarea(attrs={'disabled': 'true'}))
                        else:
                            self.base_fields[x] = forms.CharField(
                                initial=y, widget=forms.TextInput(attrs={'disabled': 'true'}))


class SubmittedFormAdmin(admin.ModelAdmin):

    def get_form(self, request, obj=None, change=False, **kwargs):
        return SubmittedForm


admin.site.register(models.CreatedForms)
admin.site.register(models.SubmittedForms, SubmittedFormAdmin)
