from rest_framework import serializers


class ReadOnlySerializer(serializers.Serializer):

    def update(self, instance, validated_data):
        # not implemented
        pass

    def create(self, validated_data):
        # not implemented
        pass

