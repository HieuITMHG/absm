from rest_framework import serializers
from core.models import User, Post, Media

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

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
    

class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ['file', 'post']

        
class PostSerializer(serializers.ModelSerializer):
    creater = UserSerializer(read_only=True)
    media = MediaSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'creater', 'caption', 'created_at', 'media']
        read_only_fields = ['creater']

    def create(self, validated_data):

        media_data = validated_data.pop('media', None)
        post = Post.objects.create(**validated_data)

        if media_data:
            for media_item_data in media_data:
                Media.objects.create(post=post, **media_item_data)

        return post



        