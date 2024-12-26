from django.contrib import admin
from .models import NovaUser

# Register your models here.
admin.site.register(NovaUser)

@admin.register(SurfSpot)
class SurfSpotAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'user', 'created_at')