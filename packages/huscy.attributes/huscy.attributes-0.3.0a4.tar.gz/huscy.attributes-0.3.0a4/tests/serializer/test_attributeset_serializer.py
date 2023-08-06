import pytest

from huscy.attributes.serializer import AttributeSetSerializer

pytestmark = pytest.mark.django_db


def test_attributeset_serializer(attribute_set):
    expected = {
        'attribute_schema_version': attribute_set.attribute_schema.pk,
        'attributes': {
            'attribute1': {},
            'attribute2': 'any string',
            'attribute3': 4.5
        },
    }

    assert expected == AttributeSetSerializer(instance=attribute_set).data
