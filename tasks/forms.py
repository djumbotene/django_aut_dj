from django import forms
from .models import Tareas

class TaskForm(forms.ModelForm):
  class Meta:
    model = Tareas
    fields= ['title', 'description','important']
    widgets= {
      'title': forms.TextInput(attrs={'class':'form-control','placeholder':'Escriba un título.' }),
      'description': forms.Textarea(attrs={'class':'form-control','placeholder': 'Escriba una descripción.'}),
      'important': forms.CheckboxInput(attrs={'class':'form-check-input m-auto'}),
    }