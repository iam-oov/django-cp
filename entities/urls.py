from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from entities import views

PREFIX_VERSION_API_1 = 'api/v1'

urlpatterns = [
    path(f'{PREFIX_VERSION_API_1}/codes/<str:zip_code>/',
         views.CodeDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
