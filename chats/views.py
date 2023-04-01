from django.shortcuts import render
from rest_framework import viewsets, permissions


# Create your views here.
from rest_framework.response import Response

from authentication.models import CustomUser
from chats.models import Chat
from chats.serializers import *


class ChatViewSet(viewsets.ModelViewSet):
    permissions = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return ShortChatSerializer
        return FullChatSerializer

    def get_queryset(self):
        return Chat.objects.all()

    def list(self, request, *args, **kwargs):
        user: CustomUser = request.user
        self.serializer_class = self.get_serializer_class()
        return Response(self.serializer_class(user.chats, many=True, context={'request': request}).data)
