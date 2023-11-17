from django.urls import path

from api.views import get_form

app_name = '%(app_label)s'

urlpatterns = [
    path('get_form/', get_form, name='get_form'),
]
