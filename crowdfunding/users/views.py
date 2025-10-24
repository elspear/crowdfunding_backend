from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.views import APIView
from django.http import Http404
from .models import Profile
from .serializers import ProfileSerializer
from .permissions import IsAccountOwner

class ProfileDetail(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAccountOwner]

    def get(self, request, user_id):
        try:
            profile = Profile.objects.get(user__id=user_id)
        except Profile.DoesNotExist:
            return Response({'detail': 'Profile not found.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            serializer = ProfileSerializer(profile)
            return Response(serializer.data)
        except Exception:
            import traceback
            traceback.print_exc()
            return Response({'detail': 'Error serializing profile'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_object(self, user_id):
        try:
            return Profile.objects.get(user__id=user_id)
        except Profile.DoesNotExist:
            raise Http404

    def put(self, request, user_id):
        profile = self.get_object(user_id)
        self.check_object_permissions(request, profile)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, user_id):
        profile = self.get_object(user_id)
        self.check_object_permissions(request, profile)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)