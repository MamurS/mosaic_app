# api/serializers.py

from rest_framework import serializers
from .models import Client, Policy

# Serializers define how the data is represented in the API (e.g., as JSON).
# They also handle validation when data is sent to the server.

class PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = '__all__' # Include all fields from the Policy model

class ClientSerializer(serializers.ModelSerializer):
    # This nested serializer will include all policies related to a client.
    policies = PolicySerializer(many=True, read_only=True)

    class Meta:
        model = Client
        fields = '__all__' # Include all fields from the Client model

        # api/serializers.py

from rest_framework import serializers
from .models import Client, Policy
from django.contrib.auth.models import User # <-- Add this import

# ... (your existing PolicySerializer and ClientSerializer) ...

# Add this new serializer for the User model
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']