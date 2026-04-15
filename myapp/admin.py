from django.contrib import admin
from .models import City, WeatherRecord, CrimeIncident

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(WeatherRecord)
class WeatherRecordAdmin(admin.ModelAdmin):
    list_display = ('city', 'date', 'temp_max', 'temp_min', 'precipitation', 'source')
    list_filter = ('city', 'source', 'date')
    search_fields = ('city__name',)

@admin.register(CrimeIncident)
class CrimeIncidentAdmin(admin.ModelAdmin):
    list_display = ('date_time', 'reason', 'city', 'location')
    list_filter = ('city', 'reason')
    search_fields = ('reason', 'location', 'city__name')
    date_hierarchy = 'date_time'
