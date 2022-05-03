from django.test import TestCase, tag
from edc_base.utils import get_utcnow
from edc_constants.constants import YES, NO, FEMALE
from edc_facility.import_holidays import import_holidays
from edc_metadata.constants import REQUIRED
from edc_metadata.models import CrfMetadata
from model_mommy import mommy

from edc_appointment.models import Appointment

from ..models import OnSchedule


@tag('dose2')
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
            dose_quantity='1')

    def test_dose2_onschedule(self):
        self.assertEqual(OnSchedule.objects.filter(
            subject_identifier=self.consent.subject_identifier,
            schedule_name='esr21_fu_schedule_v3').count(), 1)

    def test_dose2_not_onschedule(self):
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
            schedule_name='esr21_fu_schedule_v3').count(), 0)

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
            dose_quantity='2')

        self.assertEqual(OnSchedule.objects.filter(
            subject_identifier=consent.subject_identifier,
            schedule_name='esr21_fu_schedule_v3').count(), 0)

    def test_dose2_appointments_created(self):
        """Assert that two appointments were created"""
        self.assertEqual(Appointment.objects.filter(
            subject_identifier=self.consent.subject_identifier).count(), 2)

    def test_dose2_metadata_creation(self):

        appointment_1070 = Appointment.objects.get(
            subject_identifier=self.consent.subject_identifier,
            visit_code='1070')

        mommy.make_recipe(
            'esr21_subject.subjectvisit',
            subject_identifier=self.consent.subject_identifier,
            report_datetime=get_utcnow(),
            appointment=appointment_1070)

        entry_required = ['vaccinationdetails', 'physicalexam', 'vitalsigns',
                          'pregnancystatus']

        for required in entry_required:
            self.assertEqual(
                CrfMetadata.objects.get(
                    model=f'esr21_subject.{required}',
                    subject_identifier=self.consent.subject_identifier,
                    visit_code='1070').entry_status, REQUIRED)
