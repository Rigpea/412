from django.contrib import admin
from .models import Profile, StatusMessage, Image

class ImageInline(admin.TabularInline):
    model = Image
    extra = 1  
class StatusMessageAdmin(admin.ModelAdmin):
    inlines = [ImageInline]

# Register the models
admin.site.register(Profile)
admin.site.register(StatusMessage, StatusMessageAdmin)