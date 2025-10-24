from rest_framework import serializers
from .models import CustomUser, Profile
from fundraisers.serializers import FundraiserSerializer, PledgeSerializer


class CustomUserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=CustomUser.ROLE_CHOICES)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'password']
        extra_kwargs = {'password': {'write_only': True}, 'date_joined': {'read_only': True}}

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


class ProfileSerializer(serializers.ModelSerializer):
    # Be defensive: use SerializerMethodField to avoid AttributeError if related_name differs
    fundraisers = serializers.SerializerMethodField()
    pledges = serializers.SerializerMethodField()

    # Frontend provides and hosts avatar images; backend stores the selected avatar key/URL
    avatar = serializers.CharField(allow_blank=True, required=False)

    class Meta:
        model = Profile
        # include `avatar` so the frontend can save / read the user's selection
        fields = ['bio', 'avatar', 'fundraisers', 'pledges']

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