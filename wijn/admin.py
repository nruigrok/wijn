from django.contrib import admin
from wijn.models import Appellation

class AppellationAdmin(admin.ModelAdmin):
    list_display = ('name', 'region')
    list_filter = ['region']
    search_fields = ['name']

admin.site.register(Appellation, AppellationAdmin)


