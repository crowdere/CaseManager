from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Case(models.Model):
    name = models.CharField(max_length=200)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-updated', 'created']
        
    #add status open inprogress closed etc
    def __str__(self):
        return self.name

class Investigation(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    case = models.ForeignKey(Case, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    #update these to be multi select from hard coded field
    state = models.CharField(max_length=200, default='New')
    priority = models.CharField(max_length=200,null=True, blank=True)
    severity = models.CharField(max_length=200,null=True, blank=True)
    #update above to be multi select from hard coded list
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name='Investigator', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    
    class Meta:
        ordering = ['-updated', 'created']

    def __str__(self):
        return self.name


##TODO Change these from Cascade to SET_NULL evenually so on delete, we dont lose
## important case notes
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    investigation = models.ForeignKey(Investigation, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-updated', 'created']

    def __str__(self):
        return self.body[0:50]