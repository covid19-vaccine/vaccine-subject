from django.contrib import admin

from edc_model_admin.model_admin_audit_fields_mixin import audit_fieldset_tuple

from .modeladmin_mixins import CrfModelAdminMixin
from ..forms import VaccinationDetailsForm
from ..models import VaccinationDetails
from ..admin_site import esr21_subject_admin


@admin.register(VaccinationDetails, site=esr21_subject_admin)
class VaccinationDetailsAdmin(CrfModelAdminMixin, admin.ModelAdmin):
    form = VaccinationDetailsForm

    fieldsets = (
        (None, {
            'fields': (
                'subject_visit',
                'report_datetime',
                'received_dose',
                'received_dose_before',
                'vaccination_site',
                'vaccination_date',
                'location',
                'location_other',
                'admin_per_protocol',
                'reason_not_per_protocol',
                'lot_number',
                'kit_serial',
                'expiry_date',
                'provider_name',
                'part_supervised',
                'adverse_event',
                'next_vaccination_date',
            ),
        }),
        audit_fieldset_tuple)

    radio_fields = {'received_dose': admin.VERTICAL,
                    'received_dose_before': admin.VERTICAL,
                    'location': admin.VERTICAL,
                    'admin_per_protocol': admin.VERTICAL,
                    'part_supervised': admin.VERTICAL,
                    'adverse_event': admin.VERTICAL}

    def render_change_form(self, request, context, add=False,
                           change=False, form_url='', obj=None):
        context.update({
            'show_save': True,
            'show_save_and_continue': False,
            'show_save_and_add_another': False,
            'show_delete': True
        })
        return super().render_change_form(request, context, add, change, form_url, obj)
