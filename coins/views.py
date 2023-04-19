from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from coins.models import Level
from coins.serializers import LevelSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_levels(request: Request):
    levels = Level.objects.all().order_by('must_coins')
    return Response(LevelSerializer(levels, many=True, context={'request': request}).data)
