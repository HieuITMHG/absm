from rest_framework import serializers
from core.models import User, Post

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
        
class PostSerializer(serializers.ModelSerializer):
    creater = UserSerializer(read_only=True)  # Use UserSerializer to serialize the creater field

    class Meta:
        model = Post
        fields = ['id', 'creater', 'caption', 'created_at']
        read_only_fields = ['creater']


        