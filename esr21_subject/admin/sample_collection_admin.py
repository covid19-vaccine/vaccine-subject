from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import esr21_subject_admin
from ..forms import SampleCollectionForm
from ..models import SampleCollection
from .modeladmin_mixins import ModelAdminMixin


@admin.register(SampleCollection, site=esr21_subject_admin)
class SampleCollectionAdmin(
    ModelAdminMixin, admin.ModelAdmin):
    form = SampleCollectionForm

    fieldsets = (
        (None, {
            'fields': [
                'sample_collected',
                'date_collected',
                'test_type',
                'test_type_other',
            ]}),
        audit_fieldset_tuple
    )

    radio_fields = {
        'sample_collected': admin.VERTICAL,
        'test_type': admin.VERTICAL, }
