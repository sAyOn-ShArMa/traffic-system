from django.contrib import admin
from django.contrib.auth.hashers import make_password
from .models import Vehicle, Accident, Violation, TrafficSignal, Operator


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


@admin.register(Operator)
class OperatorAdmin(admin.ModelAdmin):
    list_display = ('operator_id', 'name', 'role', 'is_active', 'last_login', 'created_at')
    list_filter = ('role', 'is_active')
    search_fields = ('operator_id', 'name')

    def save_model(self, request, obj, form, change):
        if not change or 'password' in form.changed_data:
            obj.password = make_password(obj.password)
        super().save_model(request, obj, form, change)


@admin.register(TrafficSignal)
class TrafficSignalAdmin(admin.ModelAdmin):
    list_display = ('name', 'state', 'lat', 'lng', 'cycle_time')
    list_filter = ('state',)
