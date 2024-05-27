from rest_framework.routers import DefaultRouter
from seller.views import *

sellerRoutes = DefaultRouter()
from django.urls import path

sellerRoutes.register("property", PropertyViewSet)
sellerRoutes.register("nearby", NearByPlaceViewSet)

urlpatterns = [
    path("like", Likes.as_view()),
    path("interest", InterestedView.as_view()),
]

urlpatterns += sellerRoutes.urls
