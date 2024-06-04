from django.contrib.auth.models import Group, User
from .models import Color, Snippet, Embroidery
from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class EmbroiderySerializer(serializers.ModelSerializer):
    class Meta:
        model = Embroidery
        fields = ['id', 'User_id', 'Name', 'Type_id',
                  'Date', 'Description', 'get_image', 'get_absolute_url', 'get_user_name', 'get_thumbnail', 'get_description']


class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html')

    class Meta:
        model = Snippet
        fields = ['url', 'id', 'highlight', 'owner',
                  'title', 'code', 'linenos', 'language', 'style']


# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=True)
#
#     class Meta:
#         model = User
#         fields = ['url', 'id', 'username', 'snippets']


class ColorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Color
        fields = ['id', 'Name', 'HEX']
