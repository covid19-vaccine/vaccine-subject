from attr import field
from django import forms
from ..models import ProtocolDeviations


class ProtocolDeviationsForm(forms.ModelForm):
    
    # esr21_form_name = forms.MultipleChoiceField(
    #     widget=forms.CheckboxSelectMultiple,
    #     label='Which form has deviations')
    
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     choices = self.custom_choices
    #     self.fields['esr21_form_name'].choices = choices    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = self.custom_choices
        self.fields['esr21_form_name'].widget = forms.CheckboxSelectMultiple(
            choices=choices
        )   

    
    class Meta:
        model = ProtocolDeviations
        fields = '__all__'
        

