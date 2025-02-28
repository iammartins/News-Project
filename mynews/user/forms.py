from django.contrib.auth.forms import UserCreationForm
from django_ckeditor_5.widgets import CKEditor5Widget
from django import forms
from .models import User

class CustomUserCreationForm(UserCreationForm):
    profile_picture = forms.ImageField(required=False)  # Optional profile picture
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': "form-control"}), required=False) # Optional bio (using a textarea)
    phone_number = forms.CharField(max_length=20, required=False)  # Optional phone number
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)  # Optional date of birth

    class Meta:
        model = User
        fields = ( 'profile_picture','first_name',  'last_name', 'email', 'username', 'bio', 'phone_number', 'date_of_birth')  # Include custom fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"class": "form-control"})
        self.fields["email"].widget.attrs.update({"class": "form-control"})
        self.fields["first_name"].widget.attrs.update({"class": "form-control"})
        self.fields["last_name"].widget.attrs.update({"class": "form-control"})
        self.fields["password1"].widget.attrs.update({"class": "form-control"})
        self.fields["password2"].widget.attrs.update({"class": "form-control"})


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['profile_picture', 'username', 'email', 'password','first_name', 'last_name', 'bio', 'phone_number', 'date_of_birth',]  # Add the fields you want to edit
        # exclude = ['password', 'is_superuser', 'is_staff', 'is_active', 'date_joined', 'last_login'] # Or exclude the default fields you dont want to edit.
        widgets = {

                "bio": CKEditor5Widget(attrs={"class": "django_ckeditor_5"}),
              
              
              }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"class": "form-control"})
        self.fields["email"].widget.attrs.update({"class": "form-control"})
        self.fields["first_name"].widget.attrs.update({"class": "form-control"})
        self.fields["last_name"].widget.attrs.update({"class": "form-control"})
        