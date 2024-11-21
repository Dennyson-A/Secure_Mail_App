from rest_framework import serializers
from .models import Message
from django.contrib.auth.models import User
from .utils import caesar_encrypt, caesar_decrypt

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['sender', 'recipient', 'subject', 'body', 'timestamp']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']  # Include required fields
        extra_kwargs = {
            'password': {'write_only': True},  # Ensure password is write-only
        }

    def create(self, validated_data):
        # Create user and hash password
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['sender', 'recipient', 'subject', 'body', 'file', 'timestamp']

    def create(self, validated_data):
        # Encrypt the message body
        validated_data['encrypted_body'] = caesar_encrypt(validated_data['body'])
        validated_data.pop('body')  # Remove plaintext body
        return super().create(validated_data)

    def to_representation(self, instance):
        # Decrypt the message body for reading
        representation = super().to_representation(instance)
        representation['body'] = caesar_decrypt(instance.encrypted_body)
        representation.pop('encrypted_body', None)  # Remove encrypted body from the response
        return representation
