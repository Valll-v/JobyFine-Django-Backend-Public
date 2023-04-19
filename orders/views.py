from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response

from .filters import OrderFilter
from .serializers import *


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_my_orders(request: Request):
    user = request.user
    queryset = user.orders.all()
    return Response(
        OrderSerializer(queryset, many=True, context={"request": request}).data
    )


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_class = OrderFilter
    search_fields = ["name", "description", ]

    def get_queryset(self):
        print(self.request.query_params)
        return Order.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateOrderSerializer
        return OrderSerializer
