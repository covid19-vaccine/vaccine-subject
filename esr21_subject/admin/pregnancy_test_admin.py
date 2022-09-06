from django.contrib import admin

from edc_model_admin.model_admin_audit_fields_mixin import audit_fieldset_tuple

from .modeladmin_mixins import CrfModelAdminMixin
from ..forms import PregnancyTestForm
from ..models import PregnancyTest
from ..admin_site import esr21_subject_admin


@admin.register(PregnancyTest, site=esr21_subject_admin)
class PregnancyTestAdmin(CrfModelAdminMixin, admin.ModelAdmin):
    form = PregnancyTestForm
    fieldsets = (
        (None, {
            'fields': (
                'subject_visit',
                'report_datetime',
                'preg_performed',
                'preg_test_type',
                'preg_date',
                'result',)}),
        audit_fieldset_tuple)

    list_display = ('preg_performed','preg_date','result')

    list_filter = ('result',)

    radio_fields = {'preg_performed': admin.VERTICAL,
                    'preg_test_type': admin.VERTICAL,
                    'result': admin.VERTICAL, }


    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context.update({
            'show_save': True,
            'show_save_and_continue': False,
            'show_save_and_add_another': False,
            'show_delete': True
        })
        return super().render_change_form(request, context, add, change, form_url, obj)