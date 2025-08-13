# api/views.py

from rest_framework import viewsets
from .models import Client, Policy
from .serializers import ClientSerializer, PolicySerializer
from rest_framework import viewsets, filters
from rest_framework.views import APIView # <-- Add this import
from rest_framework.response import Response # <-- Add this import
from rest_framework.permissions import IsAuthenticated # <-- Add this import
from .models import Client, Policy
from .serializers import ClientSerializer, PolicySerializer, UserSerializer # <-- Add UserSerializer


# ViewSets define the logic for the API endpoints.
# The ModelViewSet automatically provides CRUD (Create, Read, Update, Delete) operations.

class ClientViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows clients to be viewed or edited.
    """
    queryset = Client.objects.all().order_by('-date')
    serializer_class = ClientSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'inn']

class PolicyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows policies to be viewed or edited.
    """
    queryset = Policy.objects.all().order_by('-creationDate')
    serializer_class = PolicySerializer

# Add this new view
class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)