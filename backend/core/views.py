from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import UserSerializer, PostSerializer, MediaSerializer, FollowSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status,permissions
from core.models import User, Post, Media
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

class RegisterView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response(serializer.errors, status=400)


class LoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'error': 'Invalid username or password'}, status=401)


class LogoutView(APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh_token')

        try:
            RefreshToken(refresh_token).blacklist()
            return Response({'message': 'Successfully logged out.'}, status=200)
        except Exception as e:
            return Response({'error': 'Invalid refresh token'}, status=400)
        
class UserView(APIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serialized_user = self.serializer_class(user)
        return Response(serialized_user.data)
    
class PeopleView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class PostView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    def get(self, request):
        posts = Post.objects.all().order_by('-created_at')
        serialized_posts = PostSerializer(posts, many=True)  
        return Response(serialized_posts.data, status=status.HTTP_200_OK)
    def post(self, request):
        caption = request.data.get('caption')
        media_files = request.FILES.getlist('media')
        # Tạo bài đăng
        post = Post.objects.create(creater=request.user, caption=caption)

        for media_file in media_files:
            media = Media.objects.create(post=post, file=media_file)

        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class Follow(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = FollowSerializer(data=request.data)
        if serializer.is_valid():
            id = serializer.validated_data['id']
            followed_user = User.objects.get(pk = id)
            follower = request.user
            if followed_user != follower:
                follower.follow.add(followed_user)
                follower.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Unfollow(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = FollowSerializer(data=request.data)
        if  serializer.is_valid():
            id = serializer.validated_data['id']
            followed_user = User.objects.get(pk = id)
            follower = request.user
            if followed_user != follower:
                follower.follow.remove(followed_user)
                follower.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




            

