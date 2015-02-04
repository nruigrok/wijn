from django.contrib import admin
from wijn.models import Appellation, Score

class AppellationAdmin(admin.ModelAdmin):
    list_display = ('name', 'region')
    list_filter = ['region']
    search_fields = ['name']

admin.site.register(Appellation, AppellationAdmin)


class ScoreAdmin(admin.ModelAdmin):
    list_display = ('user', 'vraag', 'region', 'score', 'timestamp')
    list_filter = ['user']
    search_fields = ['vraag', 'region']
admin.site.register(Score, ScoreAdmin)
