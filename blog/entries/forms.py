from django import forms

from entries.models import Blog


class SelectBlogForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    blog = forms.ModelChoiceField(Blog.objects)
