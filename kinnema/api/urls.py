from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .views import FavoriteViewset, FavoriteLastEpisodes

router = routers.DefaultRouter()
router.register(r"favorites", FavoriteViewset, basename="favorites")
router.register(r"last_episodes", FavoriteLastEpisodes, basename="favorites-episodes")

urlpatterns = [
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls")),
    path("token", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify", TokenVerifyView.as_view(), name="token_verify"),
]
