from django.contrib.auth import get_user_model
from rest_framework import serializers


class ProfileSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(
    #     view_name='xauth:profile',
    #     lookup_field=USER_LOOKUP_FIELD,
    # )

    # groups = serializers.HyperlinkedRelatedField(
    #     view_name='group-detail', many=True,
    #     read_only=True,
    # )

    class Meta:
        model = get_user_model()
        fields = tuple(get_user_model().PUBLIC_READ_WRITE_FIELDS)
        read_only_fields = tuple(get_user_model().READ_ONLY_FIELDS)
