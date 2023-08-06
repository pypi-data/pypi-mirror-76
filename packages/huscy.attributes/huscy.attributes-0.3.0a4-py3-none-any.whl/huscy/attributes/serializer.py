from rest_framework import serializers

from huscy.attributes import models
from huscy.attributes.services import update_attribute_set


class AttributeSchemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AttributeSchema
        fields = (
            'created_at',
            'schema',
        )
        read_only_fields = 'created_at',

    def update(self, attribute_schema, validated_data):
        return models.AttributeSchema.objects.create(**validated_data)


class AttributeSetSerializer(serializers.ModelSerializer):
    attribute_schema_version = serializers.SerializerMethodField()
    attributes = serializers.JSONField()

    class Meta:
        model = models.AttributeSet
        fields = (
            'attribute_schema_version',
            'attributes',
        )

    def get_attribute_schema_version(self, attribute_set):
        return attribute_set.attribute_schema.pk

    def update(self, attribute_set, validated_data):
        return update_attribute_set(attribute_set, **validated_data)
