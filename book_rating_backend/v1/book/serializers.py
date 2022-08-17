from rest_framework import serializers


class AuthorSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    birth_year = serializers.IntegerField()
    death_year = serializers.IntegerField()


class BookSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=400)
    authors = AuthorSerializer(many=True)
    languages = serializers.ListField()
    download_count = serializers.IntegerField()
