from django import forms
from .models import Data_acquire
class Dataacquireform(forms.ModelForm):
    class Meta:
        model=Data_acquire
        fields=('source','destination',)
