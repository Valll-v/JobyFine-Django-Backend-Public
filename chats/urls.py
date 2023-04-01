from django.urls import path

from chats import views

urlpatterns = [
    path('', views.ChatViewSet.as_view({'get': 'list'})),
    path('<int:pk>', views.ChatViewSet.as_view({'get': 'retrieve'})),
]
