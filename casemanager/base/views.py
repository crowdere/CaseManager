from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Investigation, Case
from .forms import InvestigationForm
# Create your views here.


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else '' 

    investigations = Investigation.objects.filter(
            Q(case__name__icontains=q) |
            Q(name__icontains=q) |
            Q(description__icontains=q)
        )

    cases = Case.objects.all()
    investigation_count = investigations.count()

    context = {'investigations':investigations, 'cases':cases, 'investigation_count':investigation_count}
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