from django.contrib.auth import get_user_model
from django.contrib.auth.middleware import get_user
from django.contrib.auth.models import update_last_login
from django.http import HttpRequest, JsonResponse, HttpResponseServerError, HttpResponse
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import Token
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from authentication import utils
from authentication.models import UserCreateCode, ActivityCategory, Review
from authentication.serializers import UserCreateSerializer, MyTokenObtainPairSerializer, CodeSerializer, \
    UpdatePasswordSerializer, ActivitySerializer, UserProfileSerializer, ReviewSerializer

User = get_user_model()


@api_view(["post"])
def reset_password(request):
    serializer = UpdatePasswordSerializer(data=request.data)
    user = serializer.is_valid(raise_exception=True)
    utils.gen_code(user)
    return Response(status=status.HTTP_201_CREATED)


@api_view(["get"])
def get_categories(request):
    return Response(ActivitySerializer(ActivityCategory.objects.all(), many=True).data)


class UserViewSet(viewsets.ModelViewSet, TokenObtainPairSerializer):
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return User.objects.all()

    def get_serializer_class(self):
        if self.action == 'update':
            return CodeSerializer
        # TODO поменять
        return UserProfileSerializer

    def get_permissions(self):
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
    def retrieve(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        try:
            user = get_user(request)
            # TODO поменять
            serializer = UserProfileSerializer(user)
            print(type(serializer.data))
            # serializer = self.get_serializer(instance)
            return JsonResponse(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(f'Something goes wrong: {ex}')


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    def get_queryset(self):
        return Review.objects.all()

    def _create_review(self, request, message, mark, **extra_fields):
        print(request)
        print(get_user(request))
        # groups = extra_fields.pop('groups', [])
        # activities = extra_fields.pop('activities', [])
        # ReviewModel = apps.get_model(self.model._meta.app_label, self.model._meta.object_name)
        review = self.model(message=message, mark=mark, **extra_fields)
        review.save(using=self._db)
        # review.groups.set(groups)
        # review.activities.set(activities)
        return review

    def create_review(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        review = self.perform_create(serializer)
        print(serializer.data)
        # headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_review(self, request: HttpRequest) -> HttpResponse:
        try:
            user = get_user(request)
            # print(user.reviews)
            serializer = ReviewSerializer(user.reviews, many=True)
            # print(serializer.data)
            # return JsonResponse(serializer.data, safe=False)
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(f'Something goes wrong: {ex}')

    # def get_review(self, request: HttpRequest) -> HttpResponse:
    #     try:
    #         user = get_user(request)
    #         serializer = self.serializer_class(data=request.data)
    #         serializer.is_valid()
    #         print(serializer.validated_data)
    #         return HttpResponse(self.queryset.filter(user=user).values())
    #     except Exception as ex:
    #         return HttpResponseServerError(f'Something goes wrong: {ex}')
