from rest_framework import serializers
from .models import CustomUser, Profile
from fundraisers.serializers import FundraiserSerializer, PledgeSerializer
from django.core.exceptions import ObjectDoesNotExist


class BasicProfileSerializer(serializers.ModelSerializer):
    """A simplified profile serializer to avoid circular imports"""
    class Meta:
        model = Profile
        fields = ['bio', 'avatar', 'location']


class CustomUserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=CustomUser.ROLE_CHOICES)
    password = serializers.CharField(write_only=True)
    avatar = serializers.CharField(write_only=True, required=False, allow_blank=True)
    location = serializers.CharField(required=False, allow_blank=True)
    profile = BasicProfileSerializer(read_only=True)  # Include profile in the output

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'password', 'avatar', 'location', 'profile']
        extra_kwargs = {'password': {'write_only': True}, 'date_joined': {'read_only': True}}

    def create(self, validated_data):
        print(f"CustomUserSerializer.create received data: {validated_data}")  # Debug log
        
        # Remove avatar and location from the data going to create_user
        avatar = validated_data.pop('avatar', None)
        location = validated_data.pop('location', None)
        print(f"Extracted location: {location}, avatar: {avatar}")  # Debug log
        
        # Create the user
        user = CustomUser.objects.create_user(**validated_data)
        
        # Store avatar and location temporarily on user instance for signal to use
        user._avatar = avatar
        user._location = location
        print(f"Set user._location to: {user._location}")  # Debug log
        
        # Important: Save to trigger the signal
        user.save()
        
        # Fetch the fresh user instance with profile
        user.refresh_from_db()
        
        return user
    



class ProfileSerializer(serializers.ModelSerializer):
    # Nested serializer for user data
    user = CustomUserSerializer(read_only=True)
    username = serializers.SerializerMethodField(read_only=True)
    
    # Related fields
    fundraisers = serializers.SerializerMethodField()
    pledges = serializers.SerializerMethodField()
    
    # Profile specific fields
    avatar = serializers.CharField(
        allow_blank=True, 
        required=False,
        max_length=200
    )
    location = serializers.CharField(
        allow_blank=True,
        required=False,
        max_length=100
    )
    bio = serializers.CharField(
        allow_blank=True,
        required=False,
        style={'base_template': 'textarea.html'}
    )

    class Meta:
        model = Profile
        fields = [
            'user',
            'username',
            'bio',
            'avatar',
            'location',
            'fundraisers',
            'pledges'
        ]

    def get_username(self, obj):
        """Return username from associated user or profile."""
        return obj.user.username if obj.user else obj.username

    def get_fundraisers(self, obj):
        """Return user's owned fundraisers."""
        try:
            fundraisers = obj.user.owned_fundraisers.all()
            return FundraiserSerializer(
                fundraisers,
                many=True,
                read_only=True
            ).data
        except (AttributeError, ObjectDoesNotExist):
            return []

    def get_pledges(self, obj):
        """Return user's non-anonymous pledges."""
        try:
            pledges = obj.user.pledges.filter(anonymous=False)
            return PledgeSerializer(
                pledges,
                many=True,
                read_only=True
            ).data
        except (AttributeError, ObjectDoesNotExist):
            return []

    def validate_location(self, value):
        """Validate location field."""
        if value and len(value.strip()) > 100:
            raise serializers.ValidationError(
                "Location must be less than 100 characters."
            )
        return value.strip()

    def update(self, instance, validated_data):
        """Handle profile updates."""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance