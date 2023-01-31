from django.contrib import admin

from message_app.models import Client, Mailing, Message


@admin.register(Client)
class PostAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'comment')



@admin.register(Mailing)
class PostAdmin(admin.ModelAdmin):
    list_display = ('time_mailing_start', 'time_mailing_end', 'period_mailing', 'status')



@admin.register(Message)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'content')