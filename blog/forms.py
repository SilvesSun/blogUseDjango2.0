from django import forms
from .models import Tag


class TagForm(forms.Form):
    tag = forms.ChoiceField(choices=[], widget=forms.RadioSelect())

    class Meta:
        model = Tag
        fields = ['id', 'name']