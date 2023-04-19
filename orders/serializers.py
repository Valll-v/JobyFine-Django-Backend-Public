from rest_framework import serializers
from authentication.models import ActivityCategory
from authentication.serializers import SubActivitySerializer
from chats.models import Chat
from user_profile.serializers import ShortProfileInfoSerializer
from .models import Order, OrderFile


class CreateOrderSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    def create(self, validated_data):
        order = super(CreateOrderSerializer, self).create(validated_data)
        if order:
            files = self.initial_data.getlist('files') if type(self.initial_data) != dict else None
            print(files)
            if files:
                for file in files:
                    OrderFile.objects.create(order=order, file=file)
        return order

    class Meta:
        model = Order
        fields = ('owner', 'name', 'description', 'subcategory', 'date_start', 'date_end', 'price_from',
                  'price_to', 'region')


class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderFile
        fields = ('file', )


class ShortActivitySerializer(serializers.ModelSerializer):

    class Meta:
        model = ActivityCategory
        fields = ('id', 'description', 'photo')


class OrderSerializer(serializers.ModelSerializer):
    owner = ShortProfileInfoSerializer()
    chat_id = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    subcategory = SubActivitySerializer()
    files = FileSerializer(many=True)

    def get_chat_id(self, obj: Order):
        user = self.context.get('request').user
        if user != obj.owner:
            chat = Chat.objects.filter(users__in=[user.id]).filter(users__in=[obj.owner.id]).first()
            if chat:
                return chat.id

    def get_category(self, obj: Order):
        return ShortActivitySerializer(obj.subcategory.category).data

    class Meta:
        model = Order
        fields = ('id', 'owner', 'name', 'description', 'chat_id', 'category', 'subcategory', 'date_start',
                  'date_end', 'price_from',
                  'price_to', 'region', 'files')
