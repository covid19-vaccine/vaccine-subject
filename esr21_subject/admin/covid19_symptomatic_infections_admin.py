from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import esr21_subject_admin
from ..forms import Covid19SymptomaticInfectionsForm
from ..models import Covid19SymptomaticInfections
from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(Covid19SymptomaticInfections, site=esr21_subject_admin)
class Covid19SymptomaticInfectionsAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = Covid19SymptomaticInfectionsForm

    fieldsets = (
        (None, {
            'fields': (
                'subject_visit',
                'report_datetime',
                'symptomatic_experiences',
                'symptomatic_infections',
                'symptomatic_infections_other',
                'date_of_infection',
                'infection_status',
                'hospitalisation_visit',
                'hospitalisation_date',
            )}),
        audit_fieldset_tuple
    )

    radio_fields = {
        'symptomatic_experiences': admin.VERTICAL,
        'infection_status': admin.VERTICAL,
        'hospitalisation_visit': admin.VERTICAL, }

    filter_horizontal = ('symptomatic_infections',)

    def render_change_form(self, request, context, add=False, change=False,
                           form_url='', obj=None):
        context.update({
            'show_save': True,
            'show_save_and_continue': False,
            'show_save_and_add_another': False,
            'show_delete': True
        })
        return super().render_change_form(request, context, add, change, form_url, obj)
