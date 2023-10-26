from rest_framework import serializers
from core.models import User, Post, Media


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ['id', 'file']

class UserSerializer(serializers.ModelSerializer):
    avatar = MediaSerializer(read_only=True)
    email = serializers.EmailField(write_only=True)
    followed_by = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'follow', 'followed_by', 'avatar']

        extra_kwargs = {
            'password' : {'write_only' : True},
        }

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("Email may not be blank.")
        return value
    
    def create(self, validated_data):
        email = validated_data.pop('email', None)  
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)

        if email is not None and password is not None:
            instance.set_password(password)
            instance.email = email 

        instance.save()
        return instance
    




class PostSerializer(serializers.ModelSerializer):
    media = MediaSerializer(many=True)
    creater = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'creater', 'caption', 'created_at', 'media']
        read_only_fields = ['creater']

class FollowSerializer(serializers.Serializer):
    id = serializers.IntegerField()

        