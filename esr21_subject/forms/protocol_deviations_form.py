from django import forms
from django.apps import apps as django_apps
from ..models import ProtocolDeviations
from esr21_subject_validation.form_validators import ProtocolDeviationFormValidator
import ast
class ProtocolDeviationsForm(forms.ModelForm):
    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = self.custom_choices
        
        initial_data = {
            'deviation_form_name':'esr21_subject.adverseevent'
            }
        
        self.fields['deviation_form_name'] = forms.ChoiceField(
            label='Forms with Deviations',
            choices=choices,

            # initial={'x': dev_str for dev_str in ast.literal_eval(self.initial['deviation_form_name'])}
            
        )
        


    # def get_label_lower(info):
    #     import ast
        # esr21_subject = django_apps.get_app_config('esr21_subject')
        # list_x_mdl = []
        # dev_list = info.replace('"', '').replace("''", '')
        # x = dev_list.replace("'", '')
        # x = x.replace('[', '').replace(']', '')
        # x = x.split(',')
        # for f_n in x:
        #     f_n = f_n.strip()
        #     list_x = [x_model._meta.verbose_name for x_model in esr21_subject.get_models() if x_model._meta.label_lower == f_n]
        #     list_x_mdl += list_x
            
        # dev_form_name = ''
        # for form_name in ast.literal_eval(info):
        #     list_x_mdl.append(form_name)
        # return list_x_mdl
        

        
        
    # try prepopulate the fields
          
    form_validator_cls = ProtocolDeviationFormValidator
    
    
    class Meta:
        model = ProtocolDeviations
        fields = '__all__'
        

