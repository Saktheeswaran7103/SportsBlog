from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','slug','category','content','featured_image','published']
        widgets = {
        'title': forms.TextInput(attrs={'class':'form-control'}),
        'slug': forms.TextInput(attrs={'class':'form-control'}),
        'category': forms.Select(attrs={'class':'form-select'}),
        'content': forms.Textarea(attrs={'class':'form-control', 'rows':6}),
        'published': forms.CheckboxInput(attrs={'class':'form-check-input'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {'body': forms.Textarea(attrs={'class':'form-control','rows':3,'placeholder':'Add your comment...'})}