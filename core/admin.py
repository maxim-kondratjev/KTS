from django.contrib import admin

from core.models import Message


class MessageAdmin(admin.ModelAdmin):
    list_display = ['author', 'text']
    search_fields = ['author__username', 'text']


admin.site.register(Message, MessageAdmin)
