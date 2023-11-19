from rest_framework import serializers
from core.models import User, Post, Media, Comment


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ['id', 'file', 'post']




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
    

class CommentSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    destination = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())

    class Meta:
        model = Comment
        fields = ['id', 'owner', 'content', 'destination']


class PostSerializer(serializers.ModelSerializer):
    media = MediaSerializer(many=True)
    creater = UserSerializer(read_only=True)
    comment = CommentSerializer(many=True, source='post_comment', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'creater', 'caption', 'created_at', 'media', 'liker', 'comment']
        read_only_fields = ['creater']

class FollowSerializer(serializers.Serializer):
    id = serializers.IntegerField()


# class CommentSerializer(serializers.ModelSerializer):
#     owner = UserSerializer(read_only=True)
#     destination = PostSerializer(read_only=True)

#     class Meta:
#         model = Comment
#         fields = ['id', 'owner', 'content', 'destination']
        
