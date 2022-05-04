from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple, StackedInlineMixin, \
    ModelAdminFormAutoNumberMixin

from ..admin.modeladmin_mixins import CrfModelAdminMixin
from ..admin_site import esr21_subject_admin
from ..forms import PregOutcomeForm, OutcomeInlineForm
from ..models import PregOutcome, OutcomeInline


class OutcomeInlineAdmin(StackedInlineMixin, ModelAdminFormAutoNumberMixin,
                         admin.StackedInline):
    form = OutcomeInlineForm
    model = OutcomeInline

    extra = 0

    fieldsets = (
        (None, {
            'fields': (
                'outcome_date',
                'specify_outcome',
                'method',
                'infant_anomalies',
            )
        }),
        audit_fieldset_tuple
    )

    radio_fields = {
        'specify_outcome': admin.VERTICAL,
        'method': admin.VERTICAL,
        'infant_anomalies': admin.VERTICAL,
    }


@admin.register(PregOutcome, site=esr21_subject_admin)
class PregOutcomeAdmin(CrfModelAdminMixin, admin.ModelAdmin):
    form = PregOutcomeForm

    inlines = [OutcomeInlineAdmin, ]

    fieldsets = (
        (None, {
            'fields': (
                'subject_visit',
                'report_datetime',
                'outcome_count',
                'comments',
            )
        }),
        audit_fieldset_tuple
    )
