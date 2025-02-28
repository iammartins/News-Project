from django import forms
from .models import Post, Comment
from django_ckeditor_5.widgets import CKEditor5Widget

class PostForm(forms.ModelForm):
    content = forms.CharField(widget = CKEditor5Widget(attrs={"class": "django_ckeditor_5"},))
           
    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'category'] 
        
        widgets ={
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Post Title'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
          }
        
class EditForm(forms.ModelForm):
    content = forms.CharField(widget = CKEditor5Widget(attrs={"class": "django_ckeditor_5"},))
    class Meta:
        model = Post
        fields = ['title', 'category', 'image', 'content']

        widgets ={
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Post Title'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
          }
        

class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea, label="Your Comment")

    class Meta:
        model = Comment
        fields = ['content']  
