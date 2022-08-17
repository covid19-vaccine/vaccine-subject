from django import forms
from edc_base.sites.forms import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin
import pytz

from edc_appointment.form_validators import AppointmentFormValidator
from edc_appointment.models import Appointment


class AppointmentForm(SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):
    """Note, the appointment is only changed, never added, through this form.
    """

    form_validator_cls = AppointmentFormValidator

    def clean(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('appt_datetime'):

            visit_definition = self.instance.visits.get(self.instance.visit_code)

            earliest_appt_date = (self.instance.timepoint_datetime -
                                  visit_definition.rlower).astimezone(
                pytz.timezone('Africa/Gaborone')).date()
            latest_appt_date = (self.instance.timepoint_datetime +
                                visit_definition.rupper).astimezone(
                pytz.timezone('Africa/Gaborone')).date()

            appt_date = cleaned_data.get('appt_datetime').date()

            if (appt_date < earliest_appt_date and
                    self.instance.visit_code in ['1070', '1170']):
                earliest_appt_date = earliest_appt_date.strftime('%Y-%m-%d')
                latest_appt_date = latest_appt_date.strftime('%Y-%m-%d')
                raise forms.ValidationError(
                    'The appointment datetime cannot be outside the window period,'
                    f' "{earliest_appt_date} to {latest_appt_date}" please '
                    'correct. See earliest, ideal and latest datetime.')
        super().clean()

    class Meta:
        model = Appointment
        fields = '__all__'
