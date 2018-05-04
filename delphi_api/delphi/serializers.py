from rest_framework import serializers
from delphi.models import Token
from delphi.constants import STAGE_CHOICES


class CustomSerializer(serializers.ModelSerializer):

    def get_field_names(self, declared_fields, info):
        expanded_fields = super(
            CustomSerializer,
            self).get_field_names(
            declared_fields,
            info)

        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = '__all__'


# class BountySerializer(CustomSerializer):
#     bountyStage = serializers.ChoiceField(choices=STAGE_CHOICES)
#     categories = CategorySerializer(read_only=True, many=True)
#     current_market_token_data = TokenSerializer(read_only=True, source='token')
#     fulfillment_count = serializers.ReadOnlyField(source='fulfillments.count')
#
#     class Meta:
#         model = Bounty
#         fields = '__all__'
#         extra_fields = ['id']
#         extra_kwargs = {
#             'data_categories': {'write_only': True},
#             'data_issuer': {'write_only': True},
#             'data_json': {'write_only': True},
#         }
