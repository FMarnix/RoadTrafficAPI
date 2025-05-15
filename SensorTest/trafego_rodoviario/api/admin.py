# from django.contrib import admin
# from django.contrib.auth.models import Group, Permission
# from .models import RoadSegmentTraffic

# @admin.register(RoadSegmentTraffic)
# class RoadSegmentAdmin(admin.ModelAdmin):
#     list_display = ['id', 'name', 'created_at', 'start_longitude', 'start_latitude', 'end_longitude', 'end_latitude', 'length', 'speed', 'intensity']  # Campos exibidos na lista
#     search_fields = ['name'] 
#     list_filter = ['created_at'] 

# # Define the groups
# admin_group, created = Group.objects.get_or_create(name='Administrador')
# anonymous_group, created = Group.objects.get_or_create(name='Anónimo')

# # Define the permissions for each group
# admin_group.permissions.add(Permission.objects.get(codename='add_roadsegmenttraffic'))
# admin_group.permissions.add(Permission.objects.get(codename='change_roadsegmenttraffic'))
# admin_group.permissions.add(Permission.objects.get(codename='delete_roadsegmenttraffic'))
# admin_group.permissions.add(Permission.objects.get(codename='view_roadsegmenttraffic'))

# anonymous_group.permissions.add(Permission.objects.get(codename='view_roadsegmenttraffic'))

# from django.apps import AppConfig
# from django.contrib.auth.models import Group, Permission
# from django.db.utils import OperationalError

# class ApiConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'api'

#     def ready(self):
#         try:
#             # Create groups
#             admin_group, created = Group.objects.get_or_create(name='Administrador')
#             anonymous_group, created = Group.objects.get_or_create(name='Anónimo')

#             # Assign permissions to the admin group
#             admin_group.permissions.add(Permission.objects.get(codename='add_roadsegmenttraffic'))
#             admin_group.permissions.add(Permission.objects.get(codename='change_roadsegmenttraffic'))
#             admin_group.permissions.add(Permission.objects.get(codename='delete_roadsegmenttraffic'))
#             admin_group.permissions.add(Permission.objects.get(codename='view_roadsegmenttraffic'))

#             # Assign permissions to the anonymous group
#             anonymous_group.permissions.add(Permission.objects.get(codename='view_roadsegmenttraffic'))
#         except OperationalError:
#             # Handle the case where the database is not ready (e.g., during migrations)
#             pass
from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from django.db.utils import OperationalError
from .models import RoadSegment, TrafficSpeed
from django.apps import AppConfig


# Register models in the Django Admin
@admin.register(RoadSegment)
class RoadSegmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at', 'total_readings']
    search_fields = ['name']
    ordering = ['-created_at']


@admin.register(TrafficSpeed)
class TrafficSpeedAdmin(admin.ModelAdmin):
    list_display = ['id', 'road_segment', 'speed', 'timestamp', 'intensity']
    search_fields = ['road_segment__name']
    ordering = ['-timestamp']


# Create groups and assign permissions
def create_groups_and_permissions():
    try:
        # Create groups
        admin_group, created = Group.objects.get_or_create(name='Administrador')
        anonymous_group, created = Group.objects.get_or_create(name='Anónimo')

        # Assign permissions to the admin group
        admin_permissions = [
            'add_roadsegment', 'change_roadsegment', 'delete_roadsegment', 'view_roadsegment',
            'add_trafficspeed', 'change_trafficspeed', 'delete_trafficspeed', 'view_trafficspeed',
        ]
        for perm in admin_permissions:
            admin_group.permissions.add(Permission.objects.get(codename=perm))

        # Assign permissions to the anonymous group
        anonymous_permissions = [
            'view_roadsegment',
            'view_trafficspeed',
        ]
        for perm in anonymous_permissions:
            anonymous_group.permissions.add(Permission.objects.get(codename=perm))
    except OperationalError:
        # Handle the case where the database is not ready (e.g., during migrations)
        pass


# Call the function when the app is ready
class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        create_groups_and_permissions()