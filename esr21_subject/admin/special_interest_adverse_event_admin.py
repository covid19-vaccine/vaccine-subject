from django.contrib import admin
from edc_model_admin.inlines import StackedInlineMixin
from edc_model_admin import audit_fieldset_tuple
from .modeladmin_mixins import CrfModelAdminMixin
from ..forms import SpecialInterestAdverseEventRecordForm, SpecialInterestAdverseEventForm
from ..models import SpecialInterestAdverseEvent, SpecialInterestAdverseEventRecord
from ..admin_site import esr21_subject_admin


class SpecialInterestAdverseEventInlineAdmin(StackedInlineMixin,
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
