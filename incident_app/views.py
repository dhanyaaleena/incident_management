from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import IncidentSerializer, IncidentDetailSerializer
from rest_framework.response import Response
from .models import Incident, Handler
from .utils import assign_pending_incidents_with_severity

# Create your views here.


class IncidentView(APIView):
    #POST /incidents/: Report new incidents.
    def post(self, request, format=None):
        serializer = IncidentSerializer(data=request.data)
        if serializer.is_valid():
            incident = serializer.save()

            #1. High Severity Incident Handling
            handlers=Handler.objects.filter(availablity=True)
            if handlers:
                handler=handlers.first()
                incident.assigned_to=handler.name
                handler.availablity=False
                handler.save()
            else:
                #4. Handler Unavailability
                incident.status="pending"
        return Response(serializer.data)

    def get(self, request):
        incidents=Incident.objects.all().first()
        return Response(incidents)


class IncidentDetailView(APIView):
    
    #PUT /incidents/{incident_id}/: Update the status or assigned handler of an incident.
    def put(self, request, id):
        incident= Incident.objects.get(id=id)
        serializer=IncidentDetailSerializer(instance=incident, data=request.data)

        #5.Incident Escalation
        if incident.status=="pending":
            pending_incidents=Incident.objects.filter(status="pending").order_by("severity")
            if pending_incidents.first()==incident:
                handlers=Handler.objects.filter(availablity=True)
                if handlers:
                    handler=handlers.first()
                    incident.assigned_to=handler.name
                    handler.availablity=False
                    handler.save()

        #3.Updating Incident Status
        if serializer.is_valid():
            serializer.save()
            if serializer.data["status"]=="resolved":
                pending_incidents = Incident.objects.filter(status="pending").order_by("severity")
                if pending_incidents:
                    next_incident=pending_incidents.first()
                    next_incident.assigned_to=serializer.validated_data["assigned_to"]
                    next_incident.save()
        return Response(serializer.data)
