import json

from django.test import TestCase
from django.urls import reverse

from form_builders.models import CreatedForms


class TestGetForms(TestCase):
    def setUp(self):
        self.first_test_form = CreatedForms.objects.create(
            name="test_name_one",
            fields="{'first_test_field': 'first_test_value'}"
            )
        self.second_test_form = CreatedForms.objects.create(
            name="test_name_two",
            fields="{'second_test_field': 'second_test_value'}"
            )
        self.get_form_data_url = "get-form-data"

    def test_list_forms_successfully(self):
        response = self.client.get(reverse("get-forms-list"))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            [
                {'pk': 1, 'name': 'test_name_one'},
                {'pk': 2, 'name': 'test_name_two'},
            ]
        )

    def test_get_a_specific_form_successfully(self):
        response = self.client.get(
            reverse(self.get_form_data_url, kwargs={'pk': self.first_test_form.pk})
            )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {
                "id": 1, "name": "test_name_one",
                "fields": {"first_test_field": "first_test_value"}
            }
        )

    def test_trying_to_get_a_form_with_not_existing_pk(self):
        response = self.client.get(
            reverse(self.get_form_data_url, kwargs={'pk': 999})
            )
        self.assertEqual(response.status_code, 404)


class TestCreateForm(TestCase):
    def setUp(self):
        self.create_form_url = "create-new-form"

    def test_create_a_form_successfully(self):
        data = {
            "title": "newtestname",
            "fields": {"newtestfield": "newtestvalue"}
            }
        response = self.client.post(
            reverse(self.create_form_url),
            data=data,
            content_type='application/json'
            )
        all_forms = CreatedForms.objects.all()
        self.assertEqual(all_forms.count(), 1)
        self.assertEqual(response.status_code, 200)

    def test_trying_to_create_a_form_with_invalid_fields(self):
        data = {
            "invalid_field": "newtestname",
            "fields": {"newtestfield": "newtestvalue"}
            }
        response = self.client.post(
            reverse(self.create_form_url),
            data=data,
            content_type='application/json'
            )
        all_forms = CreatedForms.objects.all()
        self.assertEqual(all_forms.count(), 0)
        self.assertEqual(response.status_code, 400)

    def test_trying_to_create_a_form_with_invalid_data(self):
        data = "invalid input"
        response = self.client.post(
            reverse(self.create_form_url),
            data=data,
            content_type='application/json'
            )
        all_forms = CreatedForms.objects.all()
        self.assertEqual(all_forms.count(), 0)
        self.assertEqual(response.status_code, 400)
