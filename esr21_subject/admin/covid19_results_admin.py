from django.contrib import admin
from edc_model_admin.model_admin_audit_fields_mixin import audit_fieldset_tuple

from ..admin_site import esr21_subject_admin
from ..forms import Covid19ResultsForm
from ..models import Covid19Results
from .modeladmin_mixins import ModelAdminMixin


@admin.register(Covid19Results, site=esr21_subject_admin)
class Covid19ResultsAdmin(ModelAdminMixin, admin.ModelAdmin):
    model = Covid19Results
    form = Covid19ResultsForm

    fieldsets = (
        (None, {
            'fields': (
                'subject_visit',
                'report_datetime',
                'covid_result',
            ),
        }),
        audit_fieldset_tuple)

    radio_fields = {'covid_result': admin.VERTICAL, }

    list_display = ('subject_identifier',)

    search_fields = ('subject_identifier',)
