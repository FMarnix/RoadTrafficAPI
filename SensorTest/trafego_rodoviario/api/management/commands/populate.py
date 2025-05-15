from django.core.management.base import BaseCommand
import csv
from api.models import RoadSegment, TrafficSpeed

class Command(BaseCommand):
    help = 'Populate the database with traffic speed data'

    def handle(self, *args, **kwargs):
        with open('data/traffic_speed.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                road_segment, created = RoadSegment.objects.get_or_create(
                    id=row['ID'],
                    defaults={
                        'name': f"Segment {row['ID']}",
                    }
                )
                TrafficSpeed.objects.create(
                    road_segment=road_segment,
                    start_longitude=row['Long_start'],
                    start_latitude=row['Lat_start'],
                    end_longitude=row['Long_end'],
                    end_latitude=row['Lat_end'],
                    length=row['Length'],
                    speed=row['Speed'],
                )
        self.stdout.write(self.style.SUCCESS('Database populated successfully!'))

    def handle_sensors(self, *args, **kwargs):
        with open('data/sensors.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Sensor.objects.create(
                    id=row['id'],
                    name=row['name'],
                    uuid=row['uuid']
                )
        self.stdout.write(self.style.SUCCESS('Sensors populated successfully!'))