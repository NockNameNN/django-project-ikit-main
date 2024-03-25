from django import forms
from django.forms import ModelForm
from .models import Article

class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['name', 'description', 'characters', 'featured_image']


class ContactForm(forms.Form):
    name = forms.CharField(label='Название', max_length=20)
    email = forms.EmailField(required=False)
    message = forms.CharField(widget=forms.Textarea(), required=False)
