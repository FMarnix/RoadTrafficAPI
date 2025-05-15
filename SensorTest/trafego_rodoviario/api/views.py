from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import RoadSegment, TrafficSpeed, Car, Sensor, Observation
from .serializers import (
    RoadSegmentSerializer, 
    TrafficSpeedSerializer, 
    ObservationSerializer
)
from datetime import timedelta
from django.utils.timezone import now


class APIKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        api_key = request.headers.get('X-API-KEY') or request.GET.get('api_key')
        if api_key == "23231c7a-80a7-4810-93b3-98a18ecfbc42":
            return (None, None)
        raise AuthenticationFailed('Invalid API key')


class RoadSegmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing RoadSegment objects.
    - Administrators: Can create, read, update, and delete.
    - Anonymous users: Can only read.
    """
    queryset = RoadSegment.objects.all()
    serializer_class = RoadSegmentSerializer
    permission_classes = [DjangoModelPermissions]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['name']
    ordering_fields = ['created_at']

    def destroy(self, request, *args, **kwargs):
        """Prevent deletion if there are associated TrafficSpeed records."""
        instance = self.get_object()
        if instance.traffic_speeds.exists():
            return Response(
                {"error": "Cannot delete a road segment with associated traffic speed records."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().destroy(request, *args, **kwargs)

    def get_queryset(self):
        """
        Filter road_segments by name based in intensity/traffic speed.
        """
        queryset = super().get_queryset()
        intensity = self.request.query_params.get('intensity')
        if intensity:
            traffic_speeds = TrafficSpeed.objects.all()
            if intensity == 'elevada':
                traffic_speeds = traffic_speeds.filter(speed__lte=20)
            elif intensity == 'média':
                traffic_speeds = traffic_speeds.filter(speed__gt=20, speed__lte=50)
            elif intensity == 'baixa':
                traffic_speeds = traffic_speeds.filter(speed__gt=50)

            road_segments_ids = traffic_speeds.values_list('road_segment_id', flat=True)
            queryset = queryset.filter(id__in=road_segments_ids)
        return queryset


class TrafficSpeedViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing TrafficSpeed objects.
    - Administrators: Can create, read, update, and delete.
    - Anonymous users: Can only read.
    """
    queryset = TrafficSpeed.objects.all()
    serializer_class = TrafficSpeedSerializer
    permission_classes = [DjangoModelPermissions]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['road_segment__name']
    ordering_fields = ['timestamp']

    def get_queryset(self):
        """
        Optionally filter traffic speeds by intensity.
        """
        queryset = super().get_queryset()
        intensity = self.request.query_params.get('intensity')
        if intensity:
            if intensity == 'elevada':
                queryset = queryset.filter(speed__lte=20)
            elif intensity == 'média':
                queryset = queryset.filter(speed__gt=20, speed__lte=50)
            elif intensity == 'baixa':
                queryset = queryset.filter(speed__gt=50)
        return queryset


class BulkObservationView(APIView):
    authentication_classes = [APIKeyAuthentication]

    def post(self, request):
        data = request.data
        for record in data:
            car, _ = Car.objects.get_or_create(license_plate=record['car__license_plate'])
            sensor = Sensor.objects.get(uuid=record['sensor__uuid'])
            road_segment = RoadSegment.objects.get(id=record['road_segment'])
            Observation.objects.create(
                road_segment=road_segment,
                car=car,
                sensor=sensor,
                timestamp=record['timestamp']
            )
        return Response({"message": "Observations created successfully"}, status=status.HTTP_201_CREATED)


class CarObservationsView(APIView):
    def get(self, request, license_plate):
        car = Car.objects.filter(license_plate=license_plate).first()
        if not car:
            return Response({"error": "Car not found"}, status=status.HTTP_404_NOT_FOUND)

        observations = Observation.objects.filter(
            car=car,
            timestamp__gte=now() - timedelta(hours=24)
        )
        serializer = ObservationSerializer(observations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)