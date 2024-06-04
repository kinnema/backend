from adrf import viewsets as adrf_viewsets
from django.http import HttpResponse
from django.utils.cache import patch_cache_control
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Favorite
from .serializers import FavoriteSerializer
from .tmdb.fetch_changes import fetch_last_changes


class FavoriteViewset(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FavoriteLastEpisodes(adrf_viewsets.ViewSet):

    async def list(self, request):
        content = {"user_feed": request.user}
        response = HttpResponse(content)

        patch_cache_control(response)

        changes = await fetch_last_changes()

        return changes.to_dict()
