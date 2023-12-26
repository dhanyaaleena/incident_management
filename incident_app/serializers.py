from rest_framework import serializers
from .models import Incident

class IncidentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Incident
        fields = ["type", "severity", "description"]


class IncidentDetailSerializer(serializers.ModelSerializer):
    assigned_to = serializers.CharField(required=False)
    status = serializers.CharField(required=False)
    severity = serializers.CharField(required=False)

    class Meta:
        model = Incident
        fields = [ "assigned_to", "status", "severity"]
