from django.apps import apps as django_apps
from django.conf import settings
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.urls.base import reverse
from django.urls.exceptions import NoReverseMatch
from django_revision.modeladmin_mixin import ModelAdminRevisionMixin
from edc_base.modeladmin_mixins import FormAsJSONModelAdminMixin
from edc_base.sites.admin import ModelAdminSiteMixin
from edc_fieldsets import FieldsetsModelAdminMixin
from edc_metadata import NextFormGetter
from edc_model_admin import (
    ModelAdminNextUrlRedirectMixin, ModelAdminFormInstructionsMixin,
    ModelAdminFormAutoNumberMixin, ModelAdminAuditFieldsMixin,
    ModelAdminReadOnlyMixin, ModelAdminInstitutionMixin,
    ModelAdminRedirectOnDeleteMixin)
from edc_visit_tracking.modeladmin_mixins import (
    CrfModelAdminMixin as VisitTrackingCrfModelAdminMixin)
from simple_history.admin import SimpleHistoryAdmin

from .exportaction_mixin import ExportActionMixin


class VersionControlMixin:

    def get_form_version(self, request):

        form_versions = django_apps.get_app_config('esr21_subject').form_versions

        queryset = self.get_queryset(request)
        model_name = queryset.model._meta.label_lower
        form_version = form_versions.get(model_name)

        return mark_safe(
                f' Version: {form_version} ')

    def get_timepoint(self, request):

        appt_model = django_apps.get_model('edc_appointment.appointment')

        try:
            app_obj = appt_model.objects.get(id=request.GET.get('appointment'))
        except appt_model.DoesNotExist:
            pass
        else:
            return mark_safe(
                    f'Timepoint: <i>{app_obj.visits.get(app_obj.visit_code).title} '
                    '</i> &emsp; ')

    # visit_label indicating month and day visit is happenning


class ModelAdminMixin(ModelAdminNextUrlRedirectMixin,
                      VersionControlMixin,
                      ModelAdminFormInstructionsMixin,
                      ModelAdminFormAutoNumberMixin, ModelAdminRevisionMixin,
                      ModelAdminAuditFieldsMixin, ModelAdminReadOnlyMixin,
                      ModelAdminInstitutionMixin,
                      ModelAdminRedirectOnDeleteMixin,
                      ModelAdminSiteMixin,
                      ExportActionMixin):

    list_per_page = 10
    date_hierarchy = 'modified'
    empty_value_display = '-'
    next_form_getter_cls = NextFormGetter
    enable_nav_sidebar = False

    instructions = mark_safe(
        'Please complete the questions below. Required questions are in bold. '
        'When all required questions are complete click SAVE. <br> Based on your '
        'responses, additional questions may be required or some answers may '
        'need to be corrected.<br>')

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}

        extra_context['form_version'] = self.get_form_version(request)

        return super().add_view(
            request, form_url=form_url, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):

        extra_context = extra_context or {}

        extra_context['form_version'] = self.get_form_version(request)

        return super().change_view(
            request, object_id, form_url=form_url, extra_context=extra_context)


class CrfModelAdminMixin(VisitTrackingCrfModelAdminMixin,
                         ModelAdminMixin,
                         FieldsetsModelAdminMixin,
                         FormAsJSONModelAdminMixin,
                         SimpleHistoryAdmin,
                         admin.ModelAdmin):

    post_url_on_delete_name = settings.DASHBOARD_URL_NAMES.get(
        'subject_dashboard_url')

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}

        extra_context['timepoint'] = self.get_timepoint(request)

        return super().add_view(
            request, form_url=form_url, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):

        extra_context = extra_context or {}

        extra_context['timepoint'] = self.get_timepoint(request)

        return super().change_view(
            request, object_id, form_url=form_url, extra_context=extra_context)

    def post_url_on_delete_kwargs(self, request, obj):
        return dict(
            subject_identifier=obj.subject_identifier,
            appointment=str(obj.subject_visit.appointment.id))

    def view_on_site(self, obj):
        dashboard_url_name = settings.DASHBOARD_URL_NAMES.get(
            'subject_dashboard_url')
        try:
            url = reverse(
                dashboard_url_name, kwargs=dict(
                    subject_identifier=obj.subject_visit.subject_identifier,
                    appointment=str(obj.subject_visit.appointment.id)))
        except NoReverseMatch:
            url = super().view_on_site(obj)
        return url
