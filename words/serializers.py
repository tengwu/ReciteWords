from rest_framework import serializers
from words.models import WordJson

class WordjsonSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    spell = serializers.CharField(required=True, allow_blank=False, max_length=200)

    def create(self, validated_data):
        return WordJson.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.spell = validated_data.get('hello', instance.spell)
        instance.save()
        return instance