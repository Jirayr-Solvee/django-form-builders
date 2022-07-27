from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views


urlpatterns = [
    path("create",
        views.index,
        name="create",
        ),
    path(
        "new-form",
        csrf_exempt(views.create_form),
        name="create-new-form",
        ),
    path(
        "get-forms-list",
        csrf_exempt(views.get_forms_list),
        name="get-forms-list",
        ),
    path(
        "get-form-data/<int:pk>/",
        csrf_exempt(views.get_form),
        name="get-form-data",
        ),
    path(
        "post-form",
        csrf_exempt(views.post_form),
        name="post-form",
        ),
]
