from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ('room_name', 'branch_id', 'header_img')

    Options = []
    branches = Branch.objects.all()
    for br in branches:
        Options.append((br.branch_id, br.name))

    room_name = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class' : 'uk-input uk-display-inline','placeholder':'Enter a name for the sensor'}))
    branch_id = forms.ChoiceField(widget=forms.Select(attrs={'class' : 'uk-select'}), choices=Options)
    header_img = forms.ImageField(widget=forms.FileInput(attrs={'class' : 'uk-input','onchange': "showImg(this)", 'id': "hd_img"}))