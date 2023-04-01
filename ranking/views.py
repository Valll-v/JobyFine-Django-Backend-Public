from django.contrib.auth import get_user_model
from django.db.models import Avg
from rest_framework import viewsets, permissions
from rest_framework.response import Response

from authentication.models import CustomUser
from ranking.models import Review
from ranking.serializers import WriteReviewSerializer, GetFullRankingSerializer

User = get_user_model()


class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Review.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return WriteReviewSerializer
        return GetFullRankingSerializer

    def list(self, request, *args, **kwargs):
        user: CustomUser = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)

