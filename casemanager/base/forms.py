from django.forms import ModelForm
from .models import Investigation

class InvestigationForm(ModelForm):
    class Meta:
        model = Investigation
        fields = '__all__'
        exclude = ['host', 'participants']
