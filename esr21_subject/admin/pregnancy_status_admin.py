from django.apps import apps as django_apps
from django.contrib import admin
from django.db import models
from django.forms import Textarea
from edc_base.utils import age
from edc_fieldsets.fieldlist import Insert
from .modeladmin_mixins import CrfModelAdminMixin
from ..forms import PregnancyStatusForm
from ..models import PregnancyStatus
from ..admin_site import esr21_subject_admin


@admin.register(PregnancyStatus, site=esr21_subject_admin)
class PregnancyStatusAdmin(CrfModelAdminMixin, admin.ModelAdmin):
    form = PregnancyStatusForm

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
                'primary_amenorrhea',
                'start_date_menstrual_period',
                'expected_delivery',
                'contraceptive_usage',
                'contraceptive',
                'contraceptive_other',
            )
        }),
        ('Childbearing Potential', {
            'fields': (
                'surgically_sterilized',
                'amenorrhea_history',
                'post_menopausal',
                'post_menopausal_other',
                'child_bearing_potential',
                'comment',

            )

        }),
        ('Pregnancy History', {
            'fields': (
                'number_prev_pregnancies',
                'number_normal_pregnancies',
                'number_miscarriages',
                'date_miscarriages',
                'risk_factor',
            )

        }),
    )

    radio_fields = {'primary_amenorrhea': admin.VERTICAL,
                    'contraceptive_usage': admin.VERTICAL,
                    'surgically_sterilized': admin.VERTICAL,
                    'amenorrhea_history': admin.VERTICAL,
                    'post_menopausal_range': admin.VERTICAL,
                    'post_menopausal': admin.VERTICAL}

    filter_horizontal = ('contraceptive',)

    conditional_fieldlists = {
        'above_50': Insert('post_menopausal_range', after='amenorrhea_history',
                           section='Childbearing Potential')}

    def get_key(self, request, obj=None):
        consent_cls = django_apps.get_model('esr21_subject.informedconsent')

        try:
            consent_obj = consent_cls.objects.get(
                subject_identifier=request.GET.get('subject_identifier'))
        except consent_cls.DoesNotExist:
            pass
        else:
            try:
                visit_obj = self.visit_model.objects.get(
                    id=request.GET.get('subject_visit'))
            except self.visit_model.DoesNotExist:
                pass
            else:
                if age(consent_obj.dob, visit_obj.report_datetime).years >= 50:
                    return 'above_50'

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context.update({
            'show_save': True,
            'show_save_and_continue': False,
            'show_save_and_add_another': False,
            'show_delete': True
        })
        return super().render_change_form(request, context, add, change, form_url, obj)

