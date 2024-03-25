from django import forms
from .models import Comment, Category, Tag, Post
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class PostForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget(), label='Содержимое')

    class Meta:
        model = Post
        fields = ["name", "description", "tags", "category", "featured_image"]


class CommentForm(forms.ModelForm):
    body = forms.CharField(label="Комментарий", widget=forms.Textarea(attrs={'rows': 4}), max_length=500)

    class Meta:
        model = Comment
        fields = ['body']


class PostFilterForm(forms.Form):
    search_query = forms.CharField(label='Поиск', required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label='Выберите категорию', required=False)
    tag = forms.ModelChoiceField(queryset=Tag.objects.all(), empty_label='Выберите тег', required=False)