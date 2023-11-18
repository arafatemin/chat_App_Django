from django.contrib import admin

from .models import Room, Message

class RoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_user', 'second_user']


class MessageAdmin(admin.ModelAdmin):
    list_display = ['user', 'room', 'created_date']

admin.site.register(Room, RoomAdmin)
admin.site.register(Message, MessageAdmin)


