from django import forms
from django.apps import apps as django_apps
from ..models import ProtocolDeviations
from esr21_subject_validation.form_validators import ProtocolDeviationFormValidator
class ProtocolDeviationsForm(forms.ModelForm):
    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = self.custom_choices

        self.fields['deviation_form_name'] = forms.ChoiceField(
            label='Forms with Deviations',
            choices=choices,
        )
          
    form_validator_cls = ProtocolDeviationFormValidator
    class Meta:
        model = ProtocolDeviations
        fields = '__all__'
        

