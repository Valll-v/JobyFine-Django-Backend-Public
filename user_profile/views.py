from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response

from authentication.models import CustomUser
from user_profile.serializers import UpdateProfileSerializer, ProfileSerializer

User = get_user_model()


class ProfileActionViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(is_staff=False)

    def get_serializer_class(self):
        if self.action == 'update':
            return UpdateProfileSerializer
        elif self.action == 'retrieve':
            return ProfileSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = request.user
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = request.user
        print(instance)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        phone_number = instance.phone_number
        instance.delete()
        print(instance)
        print(User.objects.filter(phone_number=phone_number).first())
        print(CustomUser.objects.filter(phone_number=phone_number).first())

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = request.user
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(ProfileSerializer(user).data)


# class UpdatePhoneViewSet(generics.CreateAPIView, generics.UpdateAPIView):
#     permission_classes = [permissions.IsAuthenticated]
#
#     def get_serializer_class(self):
#         return UpdatePhoneSerializer
