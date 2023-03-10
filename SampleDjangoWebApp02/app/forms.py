"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))


from .models import FileUpload

class UploadForm(forms.ModelForm):
    class Meta:
        model = FileUpload
        fields = ('files',)

from .models import ImageUpload

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = ImageUpload
        fields = "__all__"



