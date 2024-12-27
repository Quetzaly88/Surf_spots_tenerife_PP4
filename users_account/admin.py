from django.contrib import admin
from .models import NovaUser
from .models import SurfSpot

# Register your models here.
admin.site.register(NovaUser)

@admin.register(SurfSpot)
class SurfSpotAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'user', 'created_at')

@admin.register(SurfSpot)
class SurfSpotAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'user', 'created_at') 