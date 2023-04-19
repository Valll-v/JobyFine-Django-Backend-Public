from django.urls import path
from coins import views


urlpatterns = [
    path('', views.get_levels),
]
