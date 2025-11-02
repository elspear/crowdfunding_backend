from rest_framework.response import Response
from rest_framework import status, permissions, generics
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.http import Http404
from .models import Profile, CustomUser
from .serializers import ProfileSerializer, CustomUserSerializer
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
        print(f"PUT request.data: {request.data}")  # Debug log
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            print(f"Valid data: {serializer.validated_data}")  # Debug log
            updated_profile = serializer.save()
            print(f"Updated profile location: {updated_profile.location}")  # Debug log
            return Response(serializer.data)
        else:
            print(f"Serializer errors: {serializer.errors}")  # Debug log
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, user_id):
        profile = self.get_object(user_id)
        self.check_object_permissions(request, profile)
        print(f"PATCH request.data: {request.data}")  # Debug log
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            print(f"Valid data: {serializer.validated_data}")  # Debug log
            updated_profile = serializer.save()
            print(f"Updated profile location: {updated_profile.location}")  # Debug log
            return Response(serializer.data)
        else:
            print(f"Serializer errors: {serializer.errors}")  # Debug log
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomAuthToken(ObtainAuthToken):
    """Custom ObtainAuthToken view that returns token and basic user info."""
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': getattr(user, 'username', None),
        })


class CustomUserList(generics.ListCreateAPIView):
    """List all users or create a new user."""
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        try:
            print(f"Create user request data: {request.data}")  # Debug log
            response = super().create(request, *args, **kwargs)
            
            # Get the created user with their profile
            user = CustomUser.objects.get(id=response.data['id'])
            serializer = CustomUserSerializer(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            import traceback
            traceback.print_exc()  # This will log to your Heroku logs
            return Response(
                {'detail': 'Error creating user: ' + str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CustomUserDetail(generics.RetrieveAPIView):
    """Retrieve a single user's public info."""
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.AllowAny]


class PublicProfileView(APIView):
    """View for public access to user profiles without authentication"""
    permission_classes = [permissions.AllowAny]

    def get(self, request, user_id):
        try:
            profile = Profile.objects.get(user__id=user_id)
            serializer = ProfileSerializer(profile)
            return Response(serializer.data)
        except Profile.DoesNotExist:
            raise Http404("Profile not found")


class CheckUsernameAvailable(APIView):
    """Check if a username is available."""
    permission_classes = [permissions.AllowAny]

    def get(self, request, username):
        exists = CustomUser.objects.filter(username=username).exists()
        return Response({"available": not exists})