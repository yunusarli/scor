from django.contrib import admin

from import_export import resources
from database_tables.models import SayimEnvanter

class SayimEnvanterResources(resources.ModelResource):
    class Meta:
        model = SayimEnvanter