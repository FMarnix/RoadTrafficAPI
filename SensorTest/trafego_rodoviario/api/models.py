from django.contrib.gis.db import models


class RoadSegment(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def total_readings(self):
        return self.traffic_speeds.count()

    class Meta:
        ordering = ["-created_at"]  # Keep ordering if 'created_at' exists


class TrafficSpeed(models.Model):
    id = models.AutoField(primary_key=True)
    road_segment = models.ForeignKey(
        RoadSegment, related_name="traffic_speeds", on_delete=models.CASCADE
    )
    start_longitude = models.DecimalField(max_digits=9, decimal_places=6)
    start_latitude = models.DecimalField(max_digits=9, decimal_places=6)
    end_longitude = models.DecimalField(max_digits=9, decimal_places=6)
    end_latitude = models.DecimalField(max_digits=9, decimal_places=6)
    length = models.DecimalField(max_digits=10, decimal_places=2)
    speed = models.DecimalField(max_digits=5, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def get_traffic_intensity(self):
        if self.speed <= 20:
            return "elevada"  # high
        elif self.speed <= 50:
            return "média"  # medium
        else:
            return "baixa"  # low

    @property
    def intensity(self):
        return self.get_traffic_intensity()

    def __str__(self):
        return f"{self.road_segment.name} - {self.speed} km/h"

    class Meta:
        ordering = ["-timestamp"]  # Default ordering by timestamp (newest first)


class Sensor(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    uuid = models.UUIDField(unique=True)

    def __str__(self):
        return self.name


class Car(models.Model):
    license_plate = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.license_plate


class Observation(models.Model):
    road_segment = models.ForeignKey(
        RoadSegment, related_name="observations", on_delete=models.CASCADE
    )
    sensor = models.ForeignKey(
        Sensor, related_name="observations", on_delete=models.CASCADE
    )
    car = models.ForeignKey(Car, related_name="observations", on_delete=models.CASCADE)
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"{self.car.license_plate} observed at {self.timestamp}"
