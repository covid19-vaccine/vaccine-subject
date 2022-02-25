from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from .modeladmin_mixins import CrfModelAdminMixin
from ..forms import DemographicsDataForm
from ..models import DemographicsData
from ..admin_site import esr21_subject_admin


@admin.register(DemographicsData, site=esr21_subject_admin)
class DemographicDataAdmin(CrfModelAdminMixin, admin.ModelAdmin):
    form = DemographicsDataForm

    fieldsets = (
        (None, {
            'fields': [
                'subject_visit',
                'report_datetime',
                'country',
                'ethnicity',
                'ethnicity_other',
                'household_members',
                'highest_education',
                'employment_status',
                'employment_status_other',
                'settlement_type',
                'marital_status',
                'marital_status_other',
                'running_water',
               ]}
         ), audit_fieldset_tuple)

    radio_fields = {'ethnicity': admin.VERTICAL,
                    'highest_education': admin.VERTICAL,
                    'employment_status': admin.VERTICAL,
                    'settlement_type': admin.VERTICAL,
                    'marital_status': admin.VERTICAL,
                    'running_water': admin.VERTICAL, }

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context.update({
            'show_save': True,
            'show_save_and_continue': False,
            'show_save_and_add_another': False,
            'show_delete': True
        })
        return super().render_change_form(request, context, add, change, form_url, obj)
