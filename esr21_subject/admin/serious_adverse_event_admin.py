from django.contrib import admin
from edc_constants.constants import YES
from edc_model_admin.inlines import StackedInlineMixin
from edc_model_admin import audit_fieldset_tuple, ModelAdminFormAutoNumberMixin
from functools import partialmethod
from .modeladmin_mixins import CrfModelAdminMixin
from ..forms import SeriousAdverseEventForm, SeriousAdverseEventRecordForm
from ..models import SeriousAdverseEventRecord, SeriousAdverseEvent, AdverseEventRecord
from ..admin_site import esr21_subject_admin


class SeriousAdverseEventRecordInlineAdmin(StackedInlineMixin, ModelAdminFormAutoNumberMixin,
                                           admin.StackedInline):
    model = SeriousAdverseEventRecord
    form = SeriousAdverseEventRecordForm

    extra = 0
    max_num = 3

    fieldsets = (
        (None, {
            'fields': [
                'ae_number',
                'sae_name',
                'sae_details',
                'start_date',
                'resolution_date',
                'date_aware_of',
                'sae_criteria',
                'ae_sdth',
                'hospitalization',
                'ae_scong',
                'ae_slife',
                'ae_sdisab',
                # 'incapacity_specify',
                'ae_smie',
                # 'medical_event_other',
                'admission_date',
                'discharge_date',
                'dthcaus_1',
                'dthcaus_2',
                'ae_sddat',
                'ae_sautop',
                'rationale',
                'describe_sae_treatmnt',
                'test_performed',
                'additional_info',
                'ad',
                'ae_caad',
                'ad1',
                'ae_caad1',
                'ad2',
                'ae_caad2',
                'ae_smedca',
                'ae_smed',
                'ae_caussp',
                'ae_sp',
            ]}
        ),)

    radio_fields = {
        'ae_sdth': admin.VERTICAL,
        'ae_scong': admin.VERTICAL,
        'ae_slife': admin.VERTICAL,
        'ae_sdisab': admin.VERTICAL,
        'ae_smie': admin.VERTICAL,
        'ae_sautop': admin.VERTICAL,
        'ae_smedca': admin.VERTICAL,
        'ae_caussp': admin.VERTICAL,
        'ae_caad': admin.VERTICAL,
        'ae_caad1': admin.VERTICAL,
        'ae_caad2': admin.VERTICAL,
        'hospitalization': admin.VERTICAL,
    }

    filter_horizontal = ('sae_criteria',)

    def get_formset(self, request, obj=None, **kwargs):
        initial = []
        ae_records = None
        subject_visit_id = request.GET.get('subject_visit')
        if subject_visit_id:
            ae_records = AdverseEventRecord.objects.filter(
                adverse_event__subject_visit__id=subject_visit_id, serious_event=YES)
            if obj:
                ae_records = self.get_difference(ae_records, obj)

            for ae_record in ae_records:
                initial.append({
                    'ae_number': ae_record.ae_number,
                    'sae_name': ae_record.ae_term
                })

        formset = super().get_formset(request, obj=obj, **kwargs)
        formset.form = self.auto_number(formset.form)
        formset.__init__ = partialmethod(formset.__init__, initial=initial)
        return formset

    def get_extra(self, request, obj=None, **kwargs):
        extra = super().get_extra(request, obj, **kwargs)
        subject_visit_id = request.GET.get('subject_visit')
        if subject_visit_id:
            ae_records = AdverseEventRecord.objects.filter(
                adverse_event__subject_visit__id=subject_visit_id, serious_event=YES)
            if not obj:
                extra = ae_records.count()
            else:
                extra = len(self.get_difference(ae_records, obj))
        return extra

    def get_difference(self, model_objs, obj=None):
        sae_record_ix = obj.seriousadverseeventrecord_set.values_list(
            'ae_number', flat=True)
        return [x for x in model_objs if x.ae_number not in sae_record_ix]


@admin.register(SeriousAdverseEvent, site=esr21_subject_admin)
class SeriousAdverseEventAdmin(CrfModelAdminMixin, admin.ModelAdmin):
    form = SeriousAdverseEventForm
    inlines = [SeriousAdverseEventRecordInlineAdmin, ]

    fieldsets = (
        (None, {
            'fields': (
                'subject_visit',
                'report_datetime',
            )
        }),
        audit_fieldset_tuple
    )

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context.update({
            'show_save': True,
            'show_save_and_continue': False,
            'show_save_and_add_another': False,
            'show_delete': True
        })
        return super().render_change_form(request, context, add, change, form_url, obj)
