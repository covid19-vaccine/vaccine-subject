from django import forms
from ..models import ScreenOut
from esr21_subject_validation.form_validators import ScreenOutFormValidator

class ScreenOutForm(forms.ModelForm):
    
    form_validator_cls = ScreenOutFormValidator
    class Meta:
        model = ScreenOut
        fields = '__all__'
