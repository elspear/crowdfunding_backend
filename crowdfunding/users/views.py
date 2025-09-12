from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, serializers
from django.http import Http404
from .models import CustomUser, Profile
from .serializers import ProfileSerializer
from .serializers import CustomUserSerializer
from .permissions import IsAccountOwner
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

class CustomUserList(APIView):
    def get(self, request): 
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        try:
            # Check if username already exists
            username = request.data.get('username')
            if CustomUser.objects.filter(username=username).exists():
                return Response(
                    {"error": "Username already exists"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Check if role is valid
            role = request.data.get('role')
            if role not in ['trainer', 'pokemon_center', 'safari_park']:
                return Response(
                    {"error": "Invalid role. Must be 'trainer', 'pokemon_center', or 'safari_park'"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer = CustomUserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except ValueError:
            return Response(
                {"error": "Invalid input. Please check your username and role."},
                status=status.HTTP_400_BAD_REQUEST
            )
            

class CustomUserDetail(APIView):
    permission_classes = [IsAccountOwner]

    def get_object(self, pk): 
        try:
            return CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            raise Http404
        
    def get(self, request, pk):
        try:
            user = self.get_object(pk)
            serializer = CustomUserSerializer(user)
            return Response(serializer.data)
        except Http404:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
    def put(self, request, pk):
        try:
            user = self.get_object(pk)
            
            # Permission check in its own try block
            try:
                self.check_object_permissions(request, user)
            except permissions.exceptions.PermissionDenied:
                return Response(
                    {"error": "You don't have permission to edit this user"},
                    status=status.HTTP_403_FORBIDDEN
                )
                
            # Prevent role changes
            if 'role' in request.data:
                return Response(
                    {"error": "Role cannot be changed after registration"},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            serializer = CustomUserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except ValueError:
            return Response(
                {"error": "Invalid input data"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
    def delete(self, request, pk):
        try:
            user = self.get_object(pk)
            
            try:
                self.check_object_permissions(request, user)
            except permissions.exceptions.PermissionDenied:
                return Response(
                    {"error": "You don't have permission to delete this user"},
                    status=status.HTTP_403_FORBIDDEN
                )
                
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Http404:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        try:
            # Check if username and password are provided
            if not request.data.get('username') or not request.data.get('password'):
                return Response(
                    {"error": "Both username and password are required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer = self.serializer_class(
                data=request.data,
                context={'request': request}
            )
            
            try:
                serializer.is_valid(raise_exception=True)
            except serializers.ValidationError:
                return Response(
                    {"error": "Invalid credentials"},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)

            return Response({
                'token': token.key,
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role,
                'created': created
            })
            
        except Exception:
            return Response(
                {"error": "Login failed. Please try again."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
class ProfileDetail(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAccountOwner]
    def get(self, request, user_id):
        try:
            profile = Profile.objects.get(user__id=user_id)
        except Profile.DoesNotExist:
            return Response({'detail': 'Profile not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
    
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