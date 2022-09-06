from django.urls import path

from . import views

urlpatterns = [
    path(
        "IHETemplateService/<str:templateUID>",
        views.ReportTemplateView.as_view(),
        name="mrrt-template",
    ),
    path(
        "IHETemplateService/",
        views.ReportTemplatesListView.as_view(),
        name="mrrt-template-list",
    ),
]
