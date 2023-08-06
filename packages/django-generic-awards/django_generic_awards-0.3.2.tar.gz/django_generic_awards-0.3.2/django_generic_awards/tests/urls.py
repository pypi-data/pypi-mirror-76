'''
This urlconf exists because Django expects ROOT_URLCONF to exist.
This helps the tests remain isolated.
'''

from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]
