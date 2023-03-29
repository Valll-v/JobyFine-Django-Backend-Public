from django.urls import path

from user_profile import views

urlpatterns = [
    path('', views.ProfileActionViewSet.as_view({'patch': 'update', 'get': 'retrieve', 'delete': 'destroy'})),
]
