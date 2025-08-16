from rest_framework import serializers
from django.apps import apps

# This fetches ALL fundraisers
class FundraiserSerializer(serializers.ModelSerializer):
       class Meta:
        model = apps.get_model('fundraisers.Fundraiser')
        fields = '__all__'

# This fetches ALL pledges
class PledgeSerializer(serializers.ModelSerializer):
       class Meta:
        model = apps.get_model('fundraisers.Pledge')
        fields = '__all__'        

class FundraiserDetailSerializer(FundraiserSerializer): #we can call from the previous fundraiser
    pledges = PledgeSerializer(many=True, read_only=True) #we only can get data, not change it
    