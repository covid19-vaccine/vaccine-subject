from django.contrib import admin

from edc_model_admin.inlines import StackedInlineMixin
from edc_model_admin.model_admin_audit_fields_mixin import audit_fieldset_tuple

from .modeladmin_mixins import CrfModelAdminMixin
from ..forms import ConcomitantMedicationForm, MedicationForm
from ..models import ConcomitantMedication, Medication
from ..admin_site import esr21_subject_admin


class MedicationInlineAdmin(StackedInlineMixin, admin.StackedInline):
    model = Medication
    form = MedicationForm

    extra = 1

    fieldsets = (
        (None, {
            'fields': (
                'administered_date',
                'medication_name',
                'atc_code',
                'dose',
                'unit',
                'unit_other',
                'frequency',
                'frequency_other',
                'route',
                'route_other',
                'reason_of_use',
                'ongoing',
                'stop_date',
                'prohibited',
                'reason_prohibited',
            )}
         ),)

    radio_fields = {'ongoing': admin.VERTICAL,
                    'prohibited': admin.VERTICAL, }


@admin.register(ConcomitantMedication, site=esr21_subject_admin)
class ConcomitantMedicationAdmin(CrfModelAdminMixin, admin.ModelAdmin):
    form = ConcomitantMedicationForm

    inlines = [MedicationInlineAdmin]

    fieldsets = (
        (None, {
            'fields': (
                'subject_visit',
                'report_datetime',
            ),
        }),
        audit_fieldset_tuple)

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context.update({
            'show_save': True,
            'show_save_and_continue': False,
            'show_save_and_add_another': False,
            'show_delete': True
        })
        return super().render_change_form(request, context, add, change, form_url, obj)
