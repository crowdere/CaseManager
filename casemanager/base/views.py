from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Investigation, Case, Message
from .forms import InvestigationForm, UserForm
import pandas as pd
from plotly.offline import plot
import plotly.express as px
from multidecoder.multidecoder import Multidecoder
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

@login_required(login_url='login')
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

@login_required(login_url='login')
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
    
    ## CHART TEST
    projects_data = []
    
    # We need to itterate through all cases to check if its open, on-going, or closed
    # Open means new most likely, on-going means not closed and we take last message time, closed means closed time should be not null
    # we should also do front end to lock comments if closed.
    for x in investigations:
        #If the close time (#TODO ADD CLOSE TIME) is null, lets use their last message as the last
        # date since the case is on-going
        # if its a new case, lets just use the case.updated time since its brand new and is equal to its creation
        try:
            project = {'Case': x.name,
                    'Start': (x.created),
                    'Finish': (x.message_set.all()[0].updated),
                    'Analyst':str(x.host)}
        except:
                 project = {'Case': x.name,
                    'Start': (x.created),
                    'Finish': (x.updated),
                    'Analyst':str(x.host)}
        projects_data.append(project)
    try:
        df = pd.DataFrame(projects_data)
        fig = px.timeline(df, x_start="Start", x_end="Finish", y="Case", color="Analyst", height=375)
        fig.update_layout({
            'paper_bgcolor':'rgba(0,0,0,0)',
            'plot_bgcolor':'rgba(0,0,0,0)'
        })
        fig.update_layout(legend_font_color='white') 
        fig.update_layout(font_color='white') 

        #fig.update_yaxes(autorange="reversed")
        gantt_plot = plot(fig, output_type="div")
    except:
        gantt_plot = """
        <div style="min-height:275px;">
        <center>
        No Investigations to visualize...
        </center>
        </div>
        """
    ## END OF CHART TEST

    context = {'investigations':investigations,
               'cases':cases,
               'investigation_count':investigation_count,
               'investigation_messages':investigation_messages,
               'plot_div': gantt_plot}
               
    return render(request, 'base/home.html', context)


@login_required(login_url='login')
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

    #Indicator extraction
    md = Multidecoder()
    indicators = []
    for message in investigation_messages:
        context_tree = md.scan(str.encode(message.body))       
        for item in context_tree:
            indicators.append({'type':item['type'], 'value':item['value']})
            print(indicators)
    
    ## Report look up from ahmads part - switch this to JS front end
    reports = [{'title':'CVE-2015-0097 Exploited in the Wild', 'url':'https://www.fireeye.com/blog/threat-research/2015/07/cve-2015-0097_exploi.html'},
               {'title':'How Can I Tell if a URL is Safe?', 'url':'https://www.webroot.com/ca/en/resources/tips-articles/how-can-i-tell-if-a-url-is-safe'},]
    ##
    context = {'investigation': investigation,
     'investigation_messages': investigation_messages,
      'participants':participants,
      'indicators':indicators,
      'reports':reports}
    return render(request, 'base/investigation.html', context)


@login_required(login_url='login')
def userProfile(request,pk):
    user = User.objects.get(id=pk)
    investigations = user.investigation_set.all()
    investigation_messages = user.message_set.all()
    cases = Case.objects.all()

    context = {'user':user,
               'investigations': investigations,
               'investigation_messages':investigation_messages,
               'cases':cases}

    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def createInvestigation(request):
    form = InvestigationForm()
    cases = Case.objects.all()

    if request.method == 'POST':
        form = InvestigationForm(request.POST)
        case_name = request.POST.get('case')
        case, created = Case.objects.get_or_create(name=case_name) 

        Investigation.objects.create(
            host=request.user,
            case=case,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )  
        return redirect('home')
            
    context = {'form':form, 'cases':cases}
    return render(request, 'base/investigation_form.html', context)


@login_required(login_url='login')
def updateInvestigation(request, pk):
    investigation = Investigation.objects.get(id=pk)
    form = InvestigationForm(instance=investigation)
    cases = Case.objects.all()

    if request.user != investigation.host:
        return HttpResponse('You are not allowed here.')

    if request.method == 'POST':
        case_name = request.POST.get('case')
        case, created = Case.objects.get_or_create(name=case_name) 
        investigation.name = request.POST.get('name')
        investigation.case = case
        investigation.description = request.POST.get('description')
        investigation.save()
        return redirect('home')

    context = {'form': form, 'cases':cases, 'investigation':investigation}
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


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    context = {'form':form}
    return render(request, 'base/update-user.html', context)