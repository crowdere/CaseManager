from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Investigation, Case, Message
from .forms import InvestigationForm


# Create your views here.


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist!')

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist')
    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration.')
   
    context = {'form':form}
    return render(request, 'base/login_register.html', context)


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else '' 

    investigations = Investigation.objects.filter(
            Q(case__name__icontains=q) |
            Q(name__icontains=q) |
            Q(description__icontains=q)
        )

    cases = Case.objects.all()
    investigation_count = investigations.count()
    investigation_messages = Message.objects.filter(Q(investigation__case__name__icontains=q))

    context = {'investigations':investigations,
               'cases':cases,
               'investigation_count':investigation_count,
               'investigation_messages':investigation_messages}
               
    return render(request, 'base/home.html', context)



def investigation(request, pk):
    investigation = Investigation.objects.get(id=pk)
    #we can query child objects of a room. To get all the childrend we can specific the  name model_set
    investigation_messages = investigation.message_set.all().order_by('-created')
    participants = investigation.participants.all()

    if request.method == "POST":
        message = Message.objects.create(
            user = request.user,
            investigation=investigation,
            body=request.POST.get('body')
        )
        investigation.participants.add(request.user)
        return redirect('investigation', pk=investigation.id)


    context = {'investigation': investigation, 'investigation_messages': investigation_messages, 'participants':participants}
    return render(request, 'base/investigation.html', context)



def userProfile(request,pk):
    user = User.objects.get(id=pk)
    investigations = user.investigation_set.all()
    investigation_messages = user.message_set.all()
    cases = Case.objects.all()

    context = {'user':user,
               'investigations': investigations,
               'investigation_messages':investigation_messages,
               'case':cases}

    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def createInvestigation(request):
    form = InvestigationForm()

    if request.method == 'POST':
        form = InvestigationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
            
    context = {'form':form}
    return render(request, 'base/investigation_form.html', context)


@login_required(login_url='login')
def updateInvestigation(request, pk):
    investigation = Investigation.objects.get(id=pk)
    form = InvestigationForm(instance=investigation)

    if request.user != investigation.host:
        return HttpResponse('You are not allowed here.')

    if request.method == 'POST':
            form = InvestigationForm(request.POST, instance=investigation)
            if form.is_valid():
                form.save()
                return redirect('home')

    context = {'form': form}
    return render(request, 'base/investigation_form.html/', context)


@login_required(login_url='login')
def deleteInvestigation(request, pk):
    investigation = investigation = Investigation.objects.get(id=pk)
    
    if request.user != investigation.host:
        return HttpResponse('You are not allowed here.')
    
    if request.method == 'POST':
        investigation.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':investigation})


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    
    if request.user != message.user:
        return HttpResponse('You are not allowed here.')
    
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':message})