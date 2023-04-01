from rest_framework import serializers
from django.db.models import Q
from authentication.models import CustomUser
from chats.models import Chat, Message
from user_profile.serializers import ShortProfileInfoSerializer


class MessageSerializer(serializers.ModelSerializer):
    sender = ShortProfileInfoSerializer(source='owner', read_only=True)

    class Meta:
        model = Message
        fields = ('time', 'text', 'sender')


class FullChatSerializer(serializers.ModelSerializer):
    messages_list = MessageSerializer(many=True, source='messages', read_only=True)
    chat_with = serializers.SerializerMethodField()

    def get_chat_with(self, obj: Chat):
        user: CustomUser = self.context['request'].user
        user_with = obj.users.filter(~Q(id=user.id)).first()
        return ShortProfileInfoSerializer(user_with).data

    class Meta:
        model = Chat
        fields = ('chat_with', 'messages_list')


class ShortChatSerializer(serializers.ModelSerializer):
    last_msg = serializers.SerializerMethodField()
    chat_with = serializers.SerializerMethodField()

    def get_chat_with(self, obj: Chat):
        user: CustomUser = self.context['request'].user
        user_with = obj.users.filter(~Q(id=user.id)).first()
        return ShortProfileInfoSerializer(user_with).data

    def get_last_msg(self, obj: Chat):
        message = obj.messages.last()
        if message:
            return MessageSerializer(message).data

    class Meta:
        model = Chat
        fields = ('id', 'chat_with', 'last_msg')

