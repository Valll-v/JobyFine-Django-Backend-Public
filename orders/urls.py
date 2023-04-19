from django.urls import path

from orders import views

urlpatterns = [
    path('', views.OrderViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('<int:pk>', views.OrderViewSet.as_view({'delete': 'destroy'})),
    path('my_orders', views.get_my_orders),
]