from .models import Incident, Handler


#2. Multiple Incidents with Equal Severity. Should handle this case via tasks
def assign_pending_incidents_with_severity(severity):

    incidents=Incident.objects.filter(status="pending", severity=severity).order_by('timestamp')

    for incident in incidents:
        handlers=Handler.objects.filter(availablity=True)
        if handlers:
            handler=handlers.first()
            incident.assigned_to=handler.name
            incident.status="assigned"
            incident.save()
            handler.availablity=False
            handler.save()
        else:
            break
