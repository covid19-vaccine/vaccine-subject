from django.contrib import admin
from edc_model_admin.model_admin_audit_fields_mixin import audit_fieldset_tuple

from .modeladmin_mixins import ModelAdminMixin
from ..admin_site import esr21_subject_admin
from ..forms import VaccinationHistoryForm
from ..models import VaccinationHistory
from django.urls.base import reverse
from django.urls.exceptions import NoReverseMatch
from django.conf import settings


@admin.register(VaccinationHistory, site=esr21_subject_admin)
class VaccinationHistoryAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = VaccinationHistoryForm

    screening_listboard_url_name = settings.DASHBOARD_URL_NAMES.get(
        'screening_listboard_url')
    
    fieldsets = (
        (None, {
            'fields': (
                'subject_identifier',
                'report_datetime',
                'received_vaccine',
                'dose_quantity',
                'dose1_product_name',
                'dose1_product_other',
                'dose1_date',
                'dose2_product_name',
                'dose2_product_other',
                'dose2_date',
                'dose3_product_name',
                'dose3_product_other',
                'dose3_date',
                'source_of_info'
            )}),
        audit_fieldset_tuple)

    search_fields = ['subject_identifier']

    list_display = ('subject_identifier', 'report_datetime', )

    radio_fields = {
        'received_vaccine': admin.VERTICAL,
        'dose_quantity': admin.VERTICAL,
        'dose1_product_name': admin.VERTICAL,
        'dose2_product_name': admin.VERTICAL,
        'dose3_product_name': admin.VERTICAL,
        'source_of_info': admin.VERTICAL
    }

    def view_on_site(self, obj):
        try:
            url = reverse(
                self.screening_listboard_url_name,)
        except NoReverseMatch:
            url = super().view_on_site(obj)
        return url
