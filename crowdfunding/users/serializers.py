from rest_framework import serializers
from .models import CustomUser, Profile
from fundraisers.serializers import FundraiserSerializer, PledgeSerializer


class CustomUserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=CustomUser.ROLE_CHOICES)
    password = serializers.CharField(write_only=True)
    avatar = serializers.CharField(write_only=True, required=False)  # Add this line

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'password', 'avatar']
        extra_kwargs = {'password': {'write_only': True}, 'date_joined': {'read_only': True}}

    def create(self, validated_data):
        # Remove avatar from the data going to create_user
        avatar = validated_data.pop('avatar', None)
        # Create the user
        user = CustomUser.objects.create_user(**validated_data)
        # Store avatar temporarily on user instance for signal to use
        user._avatar = avatar
        return user



class ProfileSerializer(serializers.ModelSerializer):
    # Expose linked user and a top-level username so frontend can always read it.
    user = CustomUserSerializer(read_only=True)
    username = serializers.SerializerMethodField(read_only=True)

    # Keep your existing SerializerMethodFields
    fundraisers = serializers.SerializerMethodField()
    pledges = serializers.SerializerMethodField()

    # Frontend provides and hosts avatar images; backend stores the selected avatar key/URL
    avatar = serializers.CharField(allow_blank=True, required=False)

    class Meta:
        model = Profile
        # include all fields needed by frontend
        fields = ['user', 'username', 'bio', 'avatar', 'location', 'fundraisers', 'pledges']

    def get_username(self, obj):
        # Prefer the linked user's username if available
        if getattr(obj, "user", None):
            return obj.user.username
        # Fallback to a Profile.username field if you later add it
        return getattr(obj, "username", None)

    def get_fundraisers(self, obj):
        try:
            fundraisers_qs = getattr(obj.user, 'owned_fundraisers', None)
            if fundraisers_qs is None:
                return []
            # If it's a manager/queryset, serialize it
            return FundraiserSerializer(fundraisers_qs.all(), many=True, read_only=True).data
        except Exception:
            # Optionally log exception server-side here
            return []

    def get_pledges(self, obj):
        try:
            user = obj.user
            pledges_qs = getattr(user, 'pledges', None)
            if pledges_qs is None:
                return []
            return PledgeSerializer(pledges_qs.filter(anonymous=False), many=True).data
        except Exception:
            return []