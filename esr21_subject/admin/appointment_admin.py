from django.apps import apps as django_apps
from django.contrib import admin
from django.utils.safestring import mark_safe
from edc_appointment.admin import AppointmentAdmin as BaseAppointmentAdmin
from edc_appointment.admin_site import edc_appointment_admin
from edc_appointment.models import Appointment
from django.contrib.admin.sites import NotRegistered
from .modeladmin_mixins import VersionControlMixin

from ..forms import AppointmentForm

try:
    edc_appointment_admin.unregister(Appointment)
except NotRegistered:
    pass


@admin.register(Appointment, site=edc_appointment_admin)
class AppointmentAdmin(BaseAppointmentAdmin, VersionControlMixin):

    form = AppointmentForm

    enable_nav_sidebar = False
    add_form_template = "admin/esr21_subject/change_form.html"
    change_form_template = "admin/esr21_subject/change_form.html"

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}

        extra_context['form_version'] = self.get_form_version(request)

        return super().add_view(
            request, form_url=form_url, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):

        extra_context = extra_context or {}

        extra_context['form_version'] = self.get_form_version(request)

        appt_model = django_apps.get_model('edc_appointment.appointment')

        try:
            app_obj = appt_model.objects.get(id=object_id)
        except appt_model.DoesNotExist:
            pass
        else:
            extra_context['timepoint'] = mark_safe(
                        f'Timepoint: <i>{app_obj.visits.get(app_obj.visit_code).title} '
                        '</i> &emsp; ')

        return super().change_view(
            request, object_id, form_url=form_url, extra_context=extra_context)

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context.update({
            'show_save': True,
            'show_save_and_continue': False,
            'show_save_and_add_another': False,
            'show_delete': True
        })
        return super().render_change_form(request, context, add, change, form_url, obj)
