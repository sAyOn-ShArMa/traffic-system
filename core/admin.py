from django.contrib import admin
from .models import Vehicle, Accident, Violation, TrafficSignal


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('vehicle_id', 'lat', 'lng', 'speed', 'last_updated')
    search_fields = ('vehicle_id',)


@admin.register(Accident)
class AccidentAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'severity', 'road_name', 'status', 'injuries', 'time')
    list_filter = ('severity', 'status')
    search_fields = ('vehicle', 'road_name')


@admin.register(Violation)
class ViolationAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'violation_type', 'speed', 'fine_amount', 'time')
    list_filter = ('violation_type',)
    search_fields = ('vehicle',)


@admin.register(TrafficSignal)
class TrafficSignalAdmin(admin.ModelAdmin):
    list_display = ('name', 'state', 'lat', 'lng', 'cycle_time')
    list_filter = ('state',)
