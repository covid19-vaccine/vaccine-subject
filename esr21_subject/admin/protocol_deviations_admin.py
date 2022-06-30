from django.contrib import admin
from edc_model_admin.model_admin_audit_fields_mixin import audit_fieldset_tuple

from ..admin_site import esr21_subject_admin
from ..forms import ProtocolDeviationsForm
from ..models import ProtocolDeviations
from .modeladmin_mixins import ModelAdminMixin

from django.apps import apps

@admin.register(ProtocolDeviations, site=esr21_subject_admin)
class ProtocolDeviationsAdmin(ModelAdminMixin, admin.ModelAdmin):
    
    form = ProtocolDeviationsForm
    
    fieldsets = (
        (None, {
            "fields": (
                'report_datetime',
                'subject_identifier',
                'deviation_name',
                'deviation_description',
                'esr21_form_name',
                'comment',
            ),
        }),
        audit_fieldset_tuple
    )
    
    # filter_horizontal = ('subject_identifiers',)
    search_fields = ('subject_identifier',)
    
    list_display = [
        'created', 'subject_identifier', 'deviation_name','esr21_form_name']
    
    def get_form(self, request, obj=None, *args, **kwargs):
        
        form = super().get_form(request, *args, **kwargs)
        
        esr21_subject = apps.get_app_config('esr21_subject')
        
        esr21_models = {
            model.__name__: model for model in esr21_subject.get_models() if not model.__name__.__contains__('Historical') or model.__module__.__contains__('list_model')
        }
        form_choices =()
        model_key = ((val.__module__,key.lower()) for key,val in esr21_models.items() if 'list_model' not in val.__module__)
        for field_attr in model_key:
            form_choices +=((field_attr),)
        form_choices   

        form.custom_choices = form_choices
        return form
    
    
    