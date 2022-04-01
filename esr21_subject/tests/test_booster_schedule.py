from dateutil.relativedelta import relativedelta
from django.test import TestCase, tag
from edc_appointment.models import Appointment
from edc_appointment.constants import COMPLETE_APPT
from edc_base.utils import get_utcnow
from edc_constants.constants import YES, NO, FEMALE
from edc_facility.import_holidays import import_holidays
from edc_metadata.models import CrfMetadata
from edc_metadata.constants import REQUIRED
from edc_visit_tracking.constants import SCHEDULED
from model_mommy import mommy


from ..models import OnSchedule, VaccinationHistory


@tag('booster')
class TestBoosterScheduleSetup(TestCase):

    databases = '__all__'

    def setUp(self):
        import_holidays()

        mommy.make_recipe('esr21_subject.eligibilityconfirmation',)

        self.consent = mommy.make_recipe(
            'esr21_subject.informedconsent',
            subject_identifier='123-9877',
            gender=FEMALE)

        mommy.make_recipe(
            'esr21_subject.screeningeligibility',
            subject_identifier=self.consent.subject_identifier,
            symptomatic_infections_experiences=NO,
            is_eligible=True)

        mommy.make_recipe(
            'esr21_subject.vaccinationhistory',
            subject_identifier=self.consent.subject_identifier,
            received_vaccine=YES,
            dose_quantity='2')

    def test_booster_dose_onschedule(self):
        self.assertEqual(OnSchedule.objects.filter(
            subject_identifier=self.consent.subject_identifier,
            schedule_name='esr21_booster_schedule').count(), 1)

    def test_booster_dose_not_onschedule(self):
        consent = mommy.make_recipe(
            'esr21_subject.informedconsent',
            subject_identifier='123-9872')

        mommy.make_recipe(
            'esr21_subject.screeningeligibility',
            subject_identifier=consent.subject_identifier,
            is_eligible=True)

        mommy.make_recipe(
            'esr21_subject.vaccinationhistory',
            subject_identifier=consent.subject_identifier,
            received_vaccine=NO,
            dose_quantity=None)

        self.assertEqual(OnSchedule.objects.filter(
            subject_identifier=consent.subject_identifier,
            schedule_name='esr21_booster_schedule').count(), 0)

        consent = mommy.make_recipe(
            'esr21_subject.informedconsent',
            subject_identifier='123-9871')

        mommy.make_recipe(
            'esr21_subject.screeningeligibility',
            subject_identifier=consent.subject_identifier,
            is_eligible=True)

        mommy.make_recipe(
            'esr21_subject.vaccinationhistory',
            subject_identifier=consent.subject_identifier,
            received_vaccine=YES,
            dose_quantity=1)

        self.assertEqual(OnSchedule.objects.filter(
            subject_identifier=consent.subject_identifier,
            schedule_name='esr21_booster_schedule').count(), 0)

    def test_booster_appointments_created(self):
        """Assert that four appointments were created"""

        self.assertEqual(Appointment.objects.filter(
            subject_identifier=self.consent.subject_identifier).count(), 4)

    def test_metadata_creation_booster(self):

        appointment_170 = Appointment.objects.get(
            subject_identifier=self.consent.subject_identifier,
            visit_code='1170')

        mommy.make_recipe(
            'esr21_subject.subjectvisit',
            subject_identifier=self.consent.subject_identifier,
            report_datetime=get_utcnow(),
            appointment=appointment_170)

        entry_required = ['vaccinationdetails', 'physicalexam', 'vitalsigns',
                          'pregnancystatus']

        for required in entry_required:
            self.assertEqual(
                CrfMetadata.objects.get(
                    model=f'esr21_subject.{required}',
                    subject_identifier=self.consent.subject_identifier,
                    visit_code='1170').entry_status, REQUIRED)
