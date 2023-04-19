from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login
from django.db.models import Q
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.views import TokenObtainPairView

from authentication import utils
from authentication.models import ActivityCategory
from authentication.serializers import UserCreateSerializer, MyTokenObtainPairSerializer, CodeSerializer, \
    UpdatePasswordSerializer, ActivitySerializer, ProfileSerializer

User = get_user_model()


@api_view(["post"])
def reset_password(request):
    serializer = UpdatePasswordSerializer(data=request.data)
    user = serializer.is_valid(raise_exception=True)
    utils.gen_code(user)
    return Response(status=status.HTTP_201_CREATED)


@api_view(["post"])
def check_if_exists(request):
    data = request.data
    user = User.objects.filter(
        Q(phone_number=data.get("phone_number")) | Q(email=data.get("email"))
    ).first()
    print(user)
    print(User.objects.filter(email="email").first())
    if user:
        return Response(status=status.HTTP_400_BAD_REQUEST, data=["Пользователь уже существует"])
    else:
        return Response(status=status.HTTP_200_OK)


@api_view(["get"])
def get_categories(request):
    return Response(ActivitySerializer(ActivityCategory.objects.all().order_by('order_int', 'id'), many=True).data)


@api_view(["post"])
def update_pass_final(request: Request):
    if not request.user.is_authenticated:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    if not request.user.update_pass:
        return Response(status=status.HTTP_403_FORBIDDEN, data=["Невозможно сменить пароль"])
    password = str(request.data.get("password"))
    if not password:
        return Response(status=status.HTTP_400_BAD_REQUEST, data=["Введите пароль"])
    request.user.set_password(password)
    request.user.update_pass = False
    request.user.save()
    return Response(status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet, TokenObtainPairSerializer):
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return User.objects.all()

    def get_serializer_class(self):
        if self.action == 'update':
            return CodeSerializer
        elif self.action == 'retrieve':
            return ProfileSerializer
        return UserCreateSerializer

    def get_permissions(self):
        if self.action == 'retrieve':
            return [permissions.IsAuthenticated()]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        utils.gen_code(self.perform_create(serializer))
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        if request.data.get('update_passwd'):
            serializer.update_passwd = True
        user = serializer.is_valid()
        refresh = self.get_token(user)
        data = {"refresh": str(refresh), "access": str(refresh.access_token)}
        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, user)
        return Response(data)

    def perform_create(self, serializer):
        return serializer.save()

    def retrieve(self, request, *args, **kwargs):
        instance = request.user
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
