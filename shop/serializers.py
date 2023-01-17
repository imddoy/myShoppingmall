from rest_framework import serializers
from .models import Item
from django.contrib.auth.models import User

class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', )

class itemSerialzer(serializers.ModelSerializer):
    author = userSerializer(many=False, read_only=True)
    class Meta:
        model = Item
        fields = ['title', 'author','content', 'created_at']