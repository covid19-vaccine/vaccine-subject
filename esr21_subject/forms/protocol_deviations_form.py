from attr import field
from django import forms
from esr21_subject_validation import form_validators
from ..models import ProtocolDeviations
from edc_registration.models import RegisteredSubject
from esr21_subject_validation.form_validators import ProtocolDeviationFormValidator

class ProtocolDeviationsForm(forms.ModelForm):
    
    # esr21_form_name = forms.MultipleChoiceField(
    #     widget=forms.CheckboxSelectMultiple,
    #     label='Which form has deviations')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = self.custom_choices
 
        self.fields['esr21_form_name'].widget = forms.CheckboxSelectMultiple(
            choices=choices,
        ) 
          
    form_validator_cls = ProtocolDeviationFormValidator
    
    class Meta:
        model = ProtocolDeviations
        fields = '__all__'
        

