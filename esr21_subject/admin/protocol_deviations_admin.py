from django.contrib import admin
from edc_model_admin.model_admin_audit_fields_mixin import audit_fieldset_tuple

from ..admin_site import esr21_subject_admin
from ..forms import ProtocolDeviationsForm
from ..models import ProtocolDeviations
from .modeladmin_mixins import ModelAdminMixin
from edc_registration.models import RegisteredSubject

from django.apps import apps

@admin.register(ProtocolDeviations, site=esr21_subject_admin)
class ProtocolDeviationsAdmin(ModelAdminMixin, admin.ModelAdmin):
    
    form = ProtocolDeviationsForm
    
    fieldsets = (
        (None, {
            "fields": (
                'report_datetime',
                'subject_identifiers',
                'deviation_name',
                'deviation_description',
                'esr21_form_name',
                'deviation_form_name',
                'comment',
            ),
        }),
        audit_fieldset_tuple
    )
    
    filter_horizontal = ('subject_identifiers',)
        
    list_display = [
        'created', 'deviation_name','esr21_form_name','deviation_form_name']
    
    def get_form(self, request, obj=None, *args, **kwargs):
        
        form = super().get_form(request, *args, **kwargs)
        
        esr21_subject = apps.get_app_config('esr21_subject')
        
        esr21_models = {
            model._meta.verbose_name: model._meta.label_lower for model in esr21_subject.get_models() if not model.__name__.__contains__('Historical') or model.__module__.__contains__('list_model')
        }
        form_choices =()
        model_key = ((val.lower(),key) for key,val in esr21_models.items() if 'list_model' not in val)
        for field_attr in model_key:
            form_choices +=((field_attr),)
        form_choices   

        form.custom_choices = form_choices

        return form

    
    