from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Investigation
from .serializers import InvestigationSerializers, MessageSerializers


@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/investigations',
        'GET /api/investigations/:id'
    ]
    return Response(routes)

@api_view(['GET'])
def getInvestigations(request):
    investigations = Investigation.objects.all()
    serializer = InvestigationSerializers(investigations, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getInvestigation(request, pk):
    investigation = Investigation.objects.get(id=pk)
    serializer = InvestigationSerializers(investigation, many=False)
    return Response(serializer.data)

    
@api_view(['GET'])
def getInvestigationMessages(request, pk):
    investigation = Investigation.objects.get(id=pk)
    investigation_messages = investigation.message_set.all().order_by('-created')
    serializer = MessageSerializers(investigation_messages, many=True)
    return Response(serializer.data)