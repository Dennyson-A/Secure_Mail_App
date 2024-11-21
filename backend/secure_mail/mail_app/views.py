from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from .serializers import MessageSerializer, UserSerializer
from .models import Message

class RegisterUser(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginUser(APIView):
    def post(self, request):
        try:
            # Check if the user exists by email
            user = User.objects.get(email=request.data['email'])
            
            # Verify if the password matches
            if user.check_password(request.data['password']):
                # If valid, create and return a JWT token
                refresh = RefreshToken.for_user(user)
                return Response({
                    'token': str(refresh.access_token),  # Access token with timeout
                    'refresh': str(refresh),    
                    'message': 'Login successful'
                }, status=status.HTTP_200_OK)
            else:
                # If the password is incorrect
                return Response({'error': 'Invalid password'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            # If the user does not exist
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import MessageSerializer

class SendMessage(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def post(self, request):
        # Make a mutable copy of the request data
        data = request.data.copy()

        # Automatically set sender to the authenticated user
        data['sender'] = request.user.id

        # Use the serializer to validate and save the message
        serializer = MessageSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Message sent securely'}, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetMessages(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def get(self, request):
        # Fetch messages where the recipient is the current user's email
        messages = Message.objects.filter(recipient=request.user.email)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

