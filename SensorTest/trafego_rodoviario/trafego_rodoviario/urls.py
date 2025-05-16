from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from api.views import (
    RoadSegmentViewSet,
    TrafficSpeedViewSet,
    BulkObservationView,
    CarObservationsView,
)
from django.conf import settings
from django.conf.urls.static import static

# Swagger/OpenAPI schema view
schema_view = get_schema_view(
    openapi.Info(
        title="API Trafego Rodoviario",
        default_version="v1",
        description="Documentação da API Trafego Rodoviario",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email=""),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Create a router and register the viewsets
router = DefaultRouter()
router.register(r"road_segments", RoadSegmentViewSet, basename="roadsegment")
router.register(r"traffic_speeds", TrafficSpeedViewSet, basename="trafficspeed")


# Define URL patterns
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path(
        "api/observations/bulk/", BulkObservationView.as_view(), name="bulk-observation"
    ),
    path(
        "api/observations/<str:license_plate>/",
        CarObservationsView.as_view(),
        name="car-observations",
    ),
    path(
        "swagger.<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
