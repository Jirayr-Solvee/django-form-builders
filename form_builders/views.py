# Python imports
import json
import ast

# Django imports
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.template import loader
from django.shortcuts import get_object_or_404
from django.http import Http404

# Project imports
from form_builders.models import CreatedForms, SubmittedForms
from . import models


def index(request):
    template = loader.get_template("form_builders/index.html")
    return HttpResponse(template.render())


def create_form(request):
    if request.method == "POST":
        data = json.loads(request.body.decode(encoding="UTF-8"))
        created_form = models.CreatedForms.objects.create(
            name=str(data["title"]), fields=str(data["fields"]))
        serialized_form = serializers.serialize("json", [created_form])
        return JsonResponse(serialized_form, safe=False)


def get_forms_list(request):
    if request.method == "GET":
        results = []
        for form in CreatedForms.objects.all().values("pk", "name"):
            results.append(form)
        return JsonResponse(results, safe=False)


def get_form(request, pk):
    if request.method == "GET":
        try:
            form = CreatedForms.objects.values().get(pk=pk)
        except CreatedForms.DoesNotExist:
            raise Http404("Form does not exist")

        form["fields"] = ast.literal_eval(form["fields"])
        return JsonResponse(form, safe=False)


def post_form(request):
    if request.method == "POST":
        data = json.loads(request.body)
        form = get_object_or_404(CreatedForms, pk=data["form"])
        submitted_form = models.SubmittedForms.objects.create(form=form, data=str(data["data"]))
        serialized_form = serializers.serialize("json", [submitted_form])
        return HttpResponse(status=201)
