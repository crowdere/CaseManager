from django.shortcuts import render, redirect
from .models import Investigation
from .forms import InvestigationForm
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

def createInvestigation(request):
    form = InvestigationForm()

    if request.method == 'POST':
        form = InvestigationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
            
    context = {'form':form}
    return render(request, 'base/investigation_form.html', context)

def updateInvestigation(request, pk):
    investigation = Investigation.objects.get(id=pk)
    form = InvestigationForm(instance=investigation)

    if request.method == 'POST':
            form = InvestigationForm(request.POST, instance=investigation)
            if form.is_valid():
                form.save()
                return redirect('home')

    context = {'form': form}
    return render(request, 'base/investigation_form.html/', context)

def deleteInvestigation(request, pk):
    investigation = investigation = Investigation.objects.get(id=pk)
    if request.method == 'POST':
        investigation.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':investigation})