from rest_framework import serializers
from django.apps import apps
from .models import SiteStats


class SiteStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteStats
        fields = [
            'total_fundraisers',
            'total_users',
            'total_pledges',
            'total_amount_pledged',
            'total_pokemon_helped',
            'last_updated'
        ]
        read_only_fields = fields


class FundraiserSerializer(serializers.ModelSerializer):
    owner_username = serializers.ReadOnlyField(source="owner.username")
    owner_role = serializers.ReadOnlyField(source="owner.role")
    owner = serializers.ReadOnlyField(source="owner.id")
    end_date = serializers.DateTimeField(allow_null=True, required=False)
    items_needed = serializers.CharField(allow_blank=True, required=False)
    progress = serializers.SerializerMethodField()
    progress_percentage = serializers.SerializerMethodField()

    class Meta:
        model = apps.get_model("fundraisers.Fundraiser")
        fields = "__all__"

    def get_progress(self, obj):
        return sum(pledge.amount for pledge in obj.pledges.all())
    
    def get_progress_percentage(self, obj):
        total = sum(pledge.amount for pledge in obj.pledges.all())
        if obj.goal > 0:  # avoid division by zero
            return round((total / obj.goal) * 100, 1)  # rounds to 1 decimal place
        return 0


class PledgeSerializer(serializers.ModelSerializer):
    supporter_role = serializers.ReadOnlyField(source="supporter.role")
    supporter = serializers.ReadOnlyField(source="supporter.id")
    supporter_username = serializers.ReadOnlyField(source="supporter.username")
    fundraiser = serializers.PrimaryKeyRelatedField(queryset=apps.get_model("fundraisers.Fundraiser").objects.all())
    comment = serializers.CharField(allow_blank=True, required=False) 

    class Meta:
        model = apps.get_model("fundraisers.Pledge")
        fields = "__all__"
        extra_fields = ['supporter_username']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['supporter_username'] = instance.supporter.username
        return representation

    def update(self, instance, validated_data):
        new_amount = validated_data.get("amount", instance.amount)
        if new_amount < instance.amount:
            raise serializers.ValidationError(
                {"amount": "You can only increase your pledge amount."}
            )
        instance.amount = validated_data.get("amount", instance.amount)
        instance.comment = validated_data.get("comment", instance.comment)
        instance.anonymous = validated_data.get("anonymous", instance.anonymous)
        instance.save()
        return instance


class FundraiserDetailSerializer(FundraiserSerializer):
    pledges = PledgeSerializer(many=True, read_only=True)

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)
        instance.pokemon = validated_data.get("pokemon", instance.pokemon)
        instance.goal = validated_data.get("goal", instance.goal)
        instance.items_needed = validated_data.get(
            "items_needed", instance.items_needed
        )
        instance.location = validated_data.get("location", instance.location)  # Add location field
        instance.image = validated_data.get("image", instance.image)
        instance.is_open = validated_data.get("is_open", instance.is_open)
        instance.owner = validated_data.get("owner", instance.owner)
        instance.save()
        return instance
