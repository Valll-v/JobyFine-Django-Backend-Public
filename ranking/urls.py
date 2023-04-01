from django.urls import path

from ranking import views

urlpatterns = [
    path('', views.ReviewViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('<int:pk>', views.ReviewViewSet.as_view({'delete': 'destroy'})),
]
