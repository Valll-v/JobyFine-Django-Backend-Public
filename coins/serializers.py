from rest_framework import serializers

from coins.models import Level


class LevelSerializer(serializers.ModelSerializer):
    is_available = serializers.SerializerMethodField()

    def get_is_available(self, obj: Level) -> bool:
        user = self.context.get('request').user
        return user.balance >= obj.must_coins

    class Meta:
        model = Level
        fields = ('name', 'must_coins', 'image', 'bw_image', 'is_available')
