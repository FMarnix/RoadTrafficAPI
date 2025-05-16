from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from django.db.utils import OperationalError
from .models import (
    RoadSegment,
    TrafficSpeed,
    Car,
    Observation,
    Sensor,
)
from django.apps import AppConfig


# Register models in the Django Admin
@admin.register(RoadSegment)
class RoadSegmentAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "created_at", "total_readings"]
    search_fields = ["name"]
    ordering = ["-created_at"]


@admin.register(TrafficSpeed)
class TrafficSpeedAdmin(admin.ModelAdmin):
    list_display = ["id", "road_segment", "speed", "timestamp", "intensity"]
    search_fields = ["road_segment__name"]
    ordering = ["-timestamp"]


admin.site.register(Sensor)
admin.site.register(Car)
admin.site.register(Observation)


# Create groups and assign permissions
def create_groups_and_permissions():
    try:
        # Create groups
        admin_group, created = Group.objects.get_or_create(name="Administrador")
        anonymous_group, created = Group.objects.get_or_create(name="Anónimo")

        # Assign permissions to the admin group
        admin_permissions = [
            "add_roadsegment",
            "change_roadsegment",
            "delete_roadsegment",
            "view_roadsegment",
            "add_trafficspeed",
            "change_trafficspeed",
            "delete_trafficspeed",
            "view_trafficspeed",
        ]
        for perm in admin_permissions:
            admin_group.permissions.add(Permission.objects.get(codename=perm))

        # Assign permissions to the anonymous group
        anonymous_permissions = [
            "view_roadsegment",
            "view_trafficspeed",
        ]
        for perm in anonymous_permissions:
            anonymous_group.permissions.add(Permission.objects.get(codename=perm))
    except OperationalError:
        # Handle the case where the database is not ready (e.g., during migrations)
        pass


# Call the function when the app is ready
class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api"

    def ready(self):
        create_groups_and_permissions()
