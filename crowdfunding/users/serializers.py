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
    fundraisers = FundraiserSerializer(many=True, read_only=True, source='user.owned_fundraisers')
    pledges = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['bio', 'profile_image', 'fundraisers', 'pledges']

    def get_pledges(self, obj):
        user = obj.user
        return PledgeSerializer(user.pledges.filter(anonymous=False), many=True).data
