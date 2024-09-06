from django.contrib import admin
from .models import Tareas 
# Register your models here.

class TaskAdmin(admin.ModelAdmin):
  readonly_fields= ("datecreated",)
  
admin.site.register(Tareas, TaskAdmin)
