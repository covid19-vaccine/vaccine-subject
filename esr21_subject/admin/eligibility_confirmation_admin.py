from django.contrib import admin

from edc_model_admin.model_admin_audit_fields_mixin import audit_fieldset_tuple

from .modeladmin_mixins import ModelAdminMixin
from ..forms import EligibilityConfirmationForm
from ..models import EligibilityConfirmation
from ..admin_site import esr21_subject_admin


@admin.register(EligibilityConfirmation, site=esr21_subject_admin)
class EligibilityConfirmationAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = EligibilityConfirmationForm
    fieldsets = (
        (None, {
            'fields': (
                'screening_identifier',
                'report_datetime',
                'participating_in_other_studies',
                'age_in_years',
                'any_vaccine_receipt',
                'received_vaccines',)}),
        audit_fieldset_tuple)

    radio_fields = {
        'received_vaccines': admin.VERTICAL,
        'any_vaccine_receipt': admin.VERTICAL,
        'participating_in_other_studies': admin.VERTICAL,
    }

    search_fields = ['screening_identifier']

    readonly_fields = ('screening_identifier',)

    list_display = ('screening_identifier', 'report_datetime', 'age_in_years',)

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context.update({
            'show_save': True,
            'show_save_and_continue': False,
            'show_save_and_add_another': False,
            'show_delete': True
        })
        return super().render_change_form(request, context, add, change, form_url, obj)
