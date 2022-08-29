from django.urls import path
from . import index

urlpatterns = [
    path('', index.main),
]