import os
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User, Permission
from django.utils.timezone import now, make_aware
from datetime import datetime, timedelta
from api.models import (
    RoadSegment, 
    TrafficSpeed,
    Car,
    Sensor,
    Observation,
)


class RoadSegmentTests(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        
        # Assign permissions to the user
        permissions = [
            'add_trafficspeed',
            'change_trafficspeed',
            'delete_trafficspeed',
            'view_trafficspeed',
            'add_roadsegment',
            'change_roadsegment',
            'delete_roadsegment',
            'view_roadsegment',
        ]
        for perm in permissions:
            self.user.user_permissions.add(Permission.objects.get(codename=perm))
        
        # Authenticate the test client
        self.client.force_authenticate(user=self.user)

        # Create a sample RoadSegment and TrafficSpeed
        self.road_segment = RoadSegment.objects.create(name="Test Road Segment")

    def test_create_road_segment(self):
        url = reverse('roadsegment-list')  # Endpoint for creating road segments
        data = {'name': 'New Road Segment'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(RoadSegment.objects.count(), 2)
        self.assertTrue(RoadSegment.objects.filter(name='New Road Segment').exists())

    def test_list_road_segments(self):
        url = reverse('roadsegment-list')  # Endpoint for listing road segments
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.road_segment.name)

    def test_update_road_segment(self):
        url = reverse('roadsegment-detail', kwargs={'pk': self.road_segment.pk})  # Endpoint for updating road segments
        data = {'name': 'Updated Road Segment'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(RoadSegment.objects.get(pk=self.road_segment.pk).name, 'Updated Road Segment')

    def test_delete_road_segment(self):
        url = reverse('roadsegment-detail', kwargs={'pk': self.road_segment.pk})  # Endpoint for deleting road segments
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(RoadSegment.objects.count(), 0)

    def test_filter_road_segments_by_intensity(self):
        TrafficSpeed.objects.create(
            road_segment=self.road_segment,
            start_longitude=10.0,
            start_latitude=20.0,
            end_longitude=30.0,
            end_latitude=40.0,
            length=100.0,
            speed=15.0,  # Elevated intensity
        )

        url = reverse('roadsegment-list') + '?intensity=elevada'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Road Segment')


class TrafficSpeedTests(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        
        # Assign permissions to the user
        permissions = [
            'add_trafficspeed',
            'change_trafficspeed',
            'delete_trafficspeed',
            'view_trafficspeed',
            'add_roadsegment',
            'change_roadsegment',
            'delete_roadsegment',
            'view_roadsegment',
        ]
        for perm in permissions:
            self.user.user_permissions.add(Permission.objects.get(codename=perm))
        
        # Authenticate the test client
        self.client.force_authenticate(user=self.user)

        # Create a sample RoadSegment and TrafficSpeed
        self.road_segment = RoadSegment.objects.create(name="Test Road Segment")
        self.traffic_speed = TrafficSpeed.objects.create(
            road_segment=self.road_segment,
            start_longitude=10.0,
            start_latitude=20.0,
            end_longitude=30.0,
            end_latitude=40.0,
            length=100.0,
            speed=50.0,
        )

    def test_create_traffic_speed(self):
        url = reverse('trafficspeed-list')  # Endpoint for creating traffic speeds
        data = {
            'road_segment': self.road_segment.pk,
            'start_longitude': 15.0,
            'start_latitude': 25.0,
            'end_longitude': 35.0,
            'end_latitude': 45.0,
            'length': 120.0,
            'speed': 60.0,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TrafficSpeed.objects.count(), 2)
        self.assertEqual(TrafficSpeed.objects.first().speed, 60.0)

    def test_list_traffic_speeds(self):
        url = reverse('trafficspeed-list')  # Endpoint for listing traffic speeds
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['speed'], '50.00')

    def test_update_traffic_speed(self):
        url = reverse('trafficspeed-detail', kwargs={'pk': self.traffic_speed.pk})  # Endpoint for updating traffic speeds
        data = {
            'road_segment': self.road_segment.pk,
            'start_longitude': 12.0,
            'start_latitude': 22.0,
            'end_longitude': 32.0,
            'end_latitude': 42.0,
            'length': 110.0,
            'speed': 55.0,
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(TrafficSpeed.objects.get(pk=self.traffic_speed.pk).speed, 55.0)

    def test_delete_traffic_speed(self):
        url = reverse('trafficspeed-detail', kwargs={'pk': self.traffic_speed.pk})  # Endpoint for deleting traffic speeds
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(TrafficSpeed.objects.count(), 0)


class ObservationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client.force_authenticate(user=self.user)
        self.sensor = Sensor.objects.create(name="Test Sensor", uuid="270e4cc0-d454-4b42-8682-80e87c3d163c")
        self.road_segment = RoadSegment.objects.create(name="Test Road Segment")

    def test_bulk_observation_creation(self):
        data = [
            {
                "road_segment": self.road_segment.id,
                "car__license_plate": "AA16AA",
                "timestamp": now().isoformat(),
                "sensor__uuid": str(self.sensor.uuid)
            }
        ]
        api_key = os.environ.get('API_KEY')
        response = self.client.post(
            "/api/observations/bulk/",
            data,
            format="json",
            HTTP_AUTHORIZATION=api_key
        )
        print("Requesr Headers:", self.client._credentials)
        print("Response Status Code:", response.status_code)
        print("Response Content:", response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Observation.objects.count(), 1)

    def test_car_observations(self):
        car = Car.objects.create(license_plate="AA16AA")
        Observation.objects.create(
            road_segment=self.road_segment,
            car=car,
            sensor=self.sensor,
            timestamp=now(),
        )
        response = self.client.get(f"/api/observations/{car.license_plate}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)