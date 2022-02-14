from django.apps import apps as django_apps
from django.contrib import admin
from edc_constants.constants import YES
from edc_model_admin.inlines import StackedInlineMixin
from edc_model_admin import audit_fieldset_tuple, ModelAdminFormAutoNumberMixin
from functools import partialmethod
from .modeladmin_mixins import CrfModelAdminMixin
from ..forms import SpecialInterestAdverseEventRecordForm, SpecialInterestAdverseEventForm
from ..models import SpecialInterestAdverseEvent, SpecialInterestAdverseEventRecord
from ..models import AdverseEventRecord
from ..admin_site import esr21_subject_admin


class SpecialInterestAdverseEventInlineAdmin(StackedInlineMixin, ModelAdminFormAutoNumberMixin,
                                             admin.StackedInline):

    model = SpecialInterestAdverseEventRecord
    form = SpecialInterestAdverseEventRecordForm

    extra = 0
    max_num = 3

    fieldsets = (
        ('Participants should be encouraged to report any adverse events reported in '
         'the AE form', {
             'fields': [
                 'ae_number',
                 'aesi_name',
                 'meddra_pname',
                 'meddra_pcode',
                 'meddra_version',
                 'start_date',
                 'end_date',
                 'date_aware_of',
                 'aesi_category',
                 'rationale',
                 'describe_aesi_treatmnt',
                 'additional_info',
             ]}
         ),)

    radio_fields = {
        'aesi_category': admin.VERTICAL,
    }

    def get_formset(self, request, obj=None, **kwargs):
        initial = []
        ae_records = None
        subject_visit_id = request.GET.get('subject_visit')
        version = django_apps.get_app_config('edc_meddra').version
        if subject_visit_id:
            ae_records = AdverseEventRecord.objects.filter(
                adverse_event__subject_visit__id=subject_visit_id,
                special_interest_ae=YES)
            if obj:
                ae_records = self.get_difference(ae_records, obj)

            for ae_record in ae_records:
                initial.append({
                    'ae_number': ae_record.ae_number,
                    'aesi_name': ae_record.ae_term,
                    'meddra_version': version
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
                adverse_event__subject_visit__id=subject_visit_id,
                special_interest_ae=YES)
            if not obj:
                extra = ae_records.count()
            else:
                extra = len(self.get_difference(ae_records, obj))
        return extra

    def get_difference(self, model_objs, obj=None):
        sae_record_ix = obj.specialinterestadverseeventrecord_set.values_list(
            'ae_number', flat=True)
        return [x for x in model_objs if x.ae_number not in sae_record_ix]


@admin.register(SpecialInterestAdverseEvent, site=esr21_subject_admin)
class SpecialInterestAdverseEventAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = SpecialInterestAdverseEventForm
    inlines = [SpecialInterestAdverseEventInlineAdmin, ]

    extra = 0
    max_num = 3

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
