import re
from rest_framework import serializers
from .models import Film

class FilmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = ['id', 'title', 'description', 'genre', 'director', 'calification']

    def validate_calification(self, value):
        if not (0 <= value <= 10):
            raise serializers.ValidationError('Calification must be between 0 and 10.')
        return value

    def create(self, validated_data):
        return Film.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.genre = validated_data.get('genre', instance.genre)
        instance.director = validated_data.get('director', instance.director)
        instance.calification = validated_data.get('calification', instance.calification)
        
        instance.save()
        return instance
