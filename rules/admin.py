from django.contrib import admin
from .models import Node

# Define a custom admin class to display fields nicely in the admin panel
class NodeAdmin(admin.ModelAdmin):
    list_display = ('type', 'operator', 'value', 'left', 'right')
    search_fields = ('value',)

# Register the model with the custom admin class
admin.site.register(Node, NodeAdmin)
