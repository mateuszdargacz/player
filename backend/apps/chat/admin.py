from django.contrib import admin

from .models import Chat, Message


# admin.site.register(Message)


class MessageInline(admin.StackedInline):
    model = Message
    extra = 1


class ChatAdmin(admin.ModelAdmin):
    # fields = ['nameRoom']
    fieldsets = [
        (None, {'fields': ['name_room']}),


    ]

    inlines = [MessageInline]


admin.site.register(Chat, ChatAdmin)
