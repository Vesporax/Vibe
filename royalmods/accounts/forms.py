from django import forms
from django.contrib.auth.models import User
from django.forms import inlineformset_factory
from .models import UserProfile, SocialMediaLink


class UserProfileForm(forms.ModelForm):
    """Form for editing user profile information"""
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    
    class Meta:
        model = UserProfile
        fields = ['self_presentation']
        widgets = {
            'self_presentation': forms.Textarea(attrs={'rows': 4})
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            user = self.instance.user
            self.fields['username'].initial = user.username
            self.fields['email'].initial = user.email
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
    
    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            user = profile.user
            user.username = self.cleaned_data['username']
            user.email = self.cleaned_data['email']
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.save()
            profile.save()
        return profile


class SocialMediaLinkForm(forms.ModelForm):
    """Form for individual social media links"""
    class Meta:
        model = SocialMediaLink
        fields = ['platform', 'url', 'display_name']
        widgets = {
            'platform': forms.Select(attrs={'class': 'form-control'}),
            'url': forms.URLInput(attrs={'class': 'form-control'}),
            'display_name': forms.TextInput(attrs={'class': 'form-control'})
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['display_name'].widget.attrs['placeholder'] = 'Required for "Other" platforms'


SocialMediaFormSet = inlineformset_factory(
    User, 
    SocialMediaLink, 
    form=SocialMediaLinkForm,
    extra=1,
    max_num=10,
    can_delete=True
)