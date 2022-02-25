from django.contrib import admin
from edc_model_admin.model_admin_audit_fields_mixin import audit_fieldset_tuple

from .modeladmin_mixins import ModelAdminMixin
from ..admin_site import esr21_subject_admin
from ..forms import ScreeningEligibilityForm
from ..models import ScreeningEligibility


@admin.register(ScreeningEligibility, site=esr21_subject_admin)
class ScreeningEligibilityAdmin(ModelAdminMixin, admin.ModelAdmin):
    form = ScreeningEligibilityForm

    fieldsets = (
        (None, {
            'fields': (
                'subject_identifier',
                'report_datetime',
                'substance_hypersensitivity',
                'pregnancy_status',
                'childbearing_potential',
                'birth_control',
                'birthcontrol_agreement',
                'thrombosis_or_thrombocytopenia',
                'guillain_barre_syndrome',
                'suspected_immuno_condition',
                'clinical_bleeding',
                'covid_symptoms',
                'symptoms_other',
                'comorbidities',
                'symptomatic_infections_experiences',
                'symptomatic_infections',
                'symptomatic_infections_other'
            )}),
        audit_fieldset_tuple)

    search_fields = ['subject_identifier']

    list_display = ('subject_identifier', 'report_datetime',)

    radio_fields = {
        'substance_hypersensitivity': admin.VERTICAL,
        'pregnancy_status': admin.VERTICAL,
        'thrombosis_or_thrombocytopenia': admin.VERTICAL,
        'guillain_barre_syndrome': admin.VERTICAL,
        'suspected_immuno_condition': admin.VERTICAL,
        'clinical_bleeding': admin.VERTICAL,
        'childbearing_potential': admin.VERTICAL,
        'birth_control': admin.VERTICAL,
        'birthcontrol_agreement': admin.VERTICAL,
        'symptomatic_infections_experiences': admin.VERTICAL,
    }

    filter_horizontal = ('covid_symptoms', 'comorbidities', 'symptomatic_infections')
