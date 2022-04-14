from django.contrib import admin
from .models import TodoList, TodoListItem
# Register your models here.

admin.site.register(TodoList)
admin.site.register(TodoListItem)
