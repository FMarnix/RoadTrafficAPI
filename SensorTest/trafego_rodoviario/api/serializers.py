from rest_framework import serializers
from .models import RoadSegment, TrafficSpeed, Car, Sensor, Observation


class TrafficSpeedSerializer(serializers.ModelSerializer):
    intensity = serializers.CharField(source="get_traffic_intensity", read_only=True)

    class Meta:
        model = TrafficSpeed
        fields = [
            "id",
            "road_segment",
            "start_longitude",
            "start_latitude",
            "end_longitude",
            "end_latitude",
            "length",
            "speed",
            "timestamp",
            "intensity",
        ]


class RoadSegmentSerializer(serializers.ModelSerializer):
    traffic_speeds = TrafficSpeedSerializer(many=True, read_only=True)
    total_readings = serializers.IntegerField(read_only=True)

    class Meta:
        model = RoadSegment
        fields = ["id", "name", "created_at", "total_readings", "traffic_speeds"]


class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ["id", "name", "uuid"]


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ["license_plate", "created_at"]


class ObservationSerializer(serializers.ModelSerializer):
    road_segment = serializers.StringRelatedField()
    car = serializers.StringRelatedField()
    sensor = serializers.StringRelatedField()

    class Meta:
        model = Observation
        fields = ["road_segment", "car", "sensor", "timestamp"]
