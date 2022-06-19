from django.contrib import admin
from .models import Investigation, Case, Message

# Register your models here.
admin.site.register(Investigation) #Room
admin.site.register(Case) #Topic
admin.site.register(Message)