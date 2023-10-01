
from django.urls import path

from . import views
urlpatterns=[
    path("adminhome", views.adminindexfunction, name="adminhome"),
]