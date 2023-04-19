from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from info.models import Question, ProjectInfo
from info.serializers import QuestionSerializer, InfoSerializer


@api_view(['GET'])
def get_info(request: Request):
    info = ProjectInfo.objects.last()
    if not info:
        return Response(status=status.HTTP_502_BAD_GATEWAY, data="Возможно, ведутся серверные работы"
                                                                 " - не обнаружено данных")
    return Response(InfoSerializer(info).data)
