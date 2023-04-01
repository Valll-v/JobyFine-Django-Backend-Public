from django.contrib.auth import get_user_model
from rest_framework import serializers, exceptions

from ranking.models import Review
from user_profile.serializers import ShortProfileInfoSerializer


User = get_user_model()


class WriteReviewSerializer(serializers.ModelSerializer):
    reviewer = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Review
        fields = ('reviewer', 'receiver', 'message', 'mark')


class GetReviewSerializer(serializers.ModelSerializer):
    reviewer_details = ShortProfileInfoSerializer(
        source='reviewer', read_only=True
    )

    class Meta:
        model = Review
        fields = ('id', 'reviewer_details', 'message', 'mark')


class GetFullRankingSerializer(serializers.ModelSerializer):
    reviews_detail = GetReviewSerializer(
        many=True, source='reviews', read_only=True
    )

    class Meta:
        model = User
        fields = ('reviews_detail', 'ranking')
