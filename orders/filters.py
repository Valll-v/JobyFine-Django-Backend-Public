from django_filters import rest_framework as filters

from orders.models import Order


class RegionInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class SubcategoryInFilter(filters.BaseInFilter, filters.NumberFilter):
    pass


class OrderFilter(filters.FilterSet):
    date_start = filters.DateFilter(field_name="date_start", lookup_expr='gte')
    date_end = filters.DateFilter(field_name="date_end", lookup_expr='lte')
    price_from = filters.NumberFilter(field_name="price_from", lookup_expr='gte')
    price_to = filters.NumberFilter(field_name="price_to", lookup_expr='lte')
    region = RegionInFilter(field_name="region")
    subcategory = SubcategoryInFilter(field_name="subcategory_id")

    class Meta:
        model = Order
        fields = []
