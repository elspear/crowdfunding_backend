from rest_framework import serializers
from django.apps import apps


class FundraiserSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')

    class Meta:
        model = apps.get_model('fundraisers.Fundraiser')
        fields = '__all__'


class PledgeSerializer(serializers.ModelSerializer):
    supporter = serializers.ReadOnlyField(source='supporter.id')
    class Meta:
        model = apps.get_model('fundraisers.Pledge')
        fields = '__all__'

        def update(self, instance, validated_data):
            instance.amount = validated_data.get('amount', instance.amount)
            instance.comment = validated_data.get('comment', instance.comment)
            instance.anonymous = validated_data.get('anonymous', instance.anonymous)
            instance.fundraiser = validated_data.get('fundraiser', instance.fundraiser)
            instance.save()
            return instance

class FundraiserDetailSerializer(FundraiserSerializer):
    pledges = PledgeSerializer(many=True, read_only=True)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.pokemon= validated_data.get('pokemon', instance.pokemon)
        instance.goal = validated_data.get('goal', instance.goal)
        instance.items_needed = validated_data.get('items_needed', instance.items_needed)
        instance.image = validated_data.get('image', instance.image)
        instance.is_open = validated_data.get('is_open', instance.is_open)
        instance.owner = validated_data.get('owner', instance.owner)
        instance.save()
        return instance
    
