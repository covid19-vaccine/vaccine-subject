from django.contrib import admin
from django.db import models
from django.forms import Textarea

from edc_model_admin import audit_fieldset_tuple
from edc_model_admin.inlines import StackedInlineMixin

from .modeladmin_mixins import CrfModelAdminMixin
from ..forms import AdverseEventForm, AdverseEventRecordForm
from ..models import AdverseEvent, AdverseEventRecord
from ..admin_site import esr21_subject_admin


class AdverseEventRecordInlineAdmin(StackedInlineMixin, admin.StackedInline):

    model = AdverseEventRecord
    form = AdverseEventRecordForm

    extra = 0

    fieldsets = (
        (None, {
             'fields': [
                 'ae_name',
                 'meddra_pname',
                 'meddra_pcode',
                 'meddra_version',
                 'event_details',
                 'start_date',
                 'stop_date',
                 'substance_hypersensitivity',
                 'status',
                 'ae_grade',
                 'study_treatmnt_rel',
                 'nonstudy_treatmnt_rel',
                 'studyproc_treatmnt_rel',
                 'action_taken',
                 'outcome',
                 'sequelae_specify',
                 'serious_event',
                 'special_interest_ae',
                 'medically_attended_ae',
                 'maae_specify',
                 'treatment_given',
                 'treatmnt_given_specify',
                 'ae_study_discontinued',
                 'discontn_dt',
                 'covid_related_ae'
             ]}
         ),)

    radio_fields = {'status': admin.VERTICAL,
                    'ae_grade': admin.VERTICAL,
                    'study_treatmnt_rel': admin.VERTICAL,
                    'nonstudy_treatmnt_rel': admin.VERTICAL,
                    'studyproc_treatmnt_rel': admin.VERTICAL,
                    'action_taken': admin.VERTICAL,
                    'outcome': admin.VERTICAL,
                    'serious_event': admin.VERTICAL,
                    'special_interest_ae': admin.VERTICAL,
                    'medically_attended_ae': admin.VERTICAL,
                    'treatment_given': admin.VERTICAL,
                    'ae_study_discontinued': admin.VERTICAL,
                    'substance_hypersensitivity': admin.VERTICAL,
                    'covid_related_ae': admin.VERTICAL, }


@admin.register(AdverseEvent, site=esr21_subject_admin)
class AdverseEventAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = AdverseEventForm
    inlines = [AdverseEventRecordInlineAdmin, ]

    formfield_overrides = {
        models.TextField: {'widget': Textarea(
            attrs={'rows': 500,
                   'cols': 70,
                   'style': 'height: 7em;'})},
    }

    fieldsets = (
        (None, {
            'fields': (
                'subject_visit',
                'report_datetime',
                'experienced_ae',
            )
        }),
        audit_fieldset_tuple
    )

    radio_fields = {'experienced_ae': admin.VERTICAL, }
