from django.forms import ModelForm
from .models import Investigation
from django.contrib.auth.models import User

class InvestigationForm(ModelForm):
    class Meta:
        model = Investigation
        fields = '__all__'
        exclude = ['host', 'participants']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']