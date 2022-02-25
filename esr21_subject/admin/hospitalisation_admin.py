from django.contrib import admin

from .modeladmin_mixins import CrfModelAdminMixin
from ..forms import HospitalisationForm
from ..models import Hospitalisation
from ..admin_site import esr21_subject_admin


@admin.register(Hospitalisation, site=esr21_subject_admin)
class HospitalisationAdmin(CrfModelAdminMixin, admin.ModelAdmin):
    model = Hospitalisation
    form = HospitalisationForm

    fieldsets = (
        (None, {
            'fields': [
                'subject_visit',
                'report_datetime',
                'status',
                'start_date',
                'ongoing',
                'stop_date',
                'reason',
                'reason_other',
                'covid_symptoms',
                'hospitalisation_outcome',
            ]}
         ),)

    radio_fields = {'status': admin.VERTICAL,
                    'ongoing': admin.VERTICAL,
                    'reason': admin.VERTICAL,
                    'hospitalisation_outcome': admin.VERTICAL, }

    filter_horizontal = ('covid_symptoms',)

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context.update({
            'show_save': True,
            'show_save_and_continue': False,
            'show_save_and_add_another': False,
            'show_delete': True
        })
        return super().render_change_form(request, context, add, change, form_url, obj)
