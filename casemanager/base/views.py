from django.shortcuts import render
from .models import Investigation
# Create your views here.


# NO LONGER USING
# investigations = [
#     {'id':1,'name':'COMP-DHG001983'},
#     {'id':2,'name':'PCAP-DHG001983'},
#     {'id':3,'name':'MEM-DHG001983'},
# ]


def home(request):
    investigations = Investigation.objects.all()
    context = {'investigations':investigations}
    return render(request, 'base/home.html', context)


def investigation(request, pk):
    investigation = Investigation.objects.get(id=pk)
    context = {'investigation': investigation}
    return render(request, 'base/investigation.html', context)