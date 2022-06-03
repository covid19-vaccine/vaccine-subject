from dateutil.relativedelta import relativedelta
from django.test import TestCase
from edc_appointment.models import Appointment
from edc_base import get_utcnow
from edc_constants.constants import FEMALE, OMANG, YES, NO
from edc_facility.import_holidays import import_holidays
from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata.models import CrfMetadata
from model_mommy import mommy

from esr21_subject.helper_classes import EnrollmentHelper


class TestConcMedication(TestCase):
    databases = '__all__'

    def setUp(self):
        import_holidays()

        self.enrol_helper = EnrollmentHelper

        self.eligibility = mommy.make_recipe(
            'esr21_subject.eligibilityconfirmation', )

        self.consent_options = {
            'screening_identifier': self.eligibility.screening_identifier,
            'consent_datetime': get_utcnow(),
            'version': 1,
            'dob': (get_utcnow() - relativedelta(years=45)).date(),
            'first_name': 'TEST ONE',
            'last_name': 'TEST',
            'initials': 'TOT',
            'identity': '123425678',
            'confirm_identity': '123425678',
            'identity_type': OMANG,
            'gender': FEMALE}

        self.consent = mommy.make_recipe(
            'esr21_subject.informedconsent',
            **self.consent_options)

        mommy.make_recipe(
            'esr21_subject.screeningeligibility',
            subject_identifier=self.consent.subject_identifier,
            is_eligible=True)

        self.subject_identifier = self.consent.subject_identifier

        mommy.make_recipe(
            'esr21_subject.vaccinationhistory',
            subject_identifier=self.consent.subject_identifier,
            received_vaccine=YES,
            dose_quantity='2', )

        self.cohort = 'esr21'
        self.schedule_enrollment = self.enrol_helper(
            cohort=self.cohort, subject_identifier=self.subject_identifier)
        self.schedule_enrollment.schedule_enrol()

        self.appointment_170 = Appointment.objects.get(
            subject_identifier=self.consent.subject_identifier,
            visit_code='1170')

        self.visit = mommy.make_recipe(
            'esr21_subject.subjectvisit',
            subject_identifier=self.consent.subject_identifier,
            report_datetime=get_utcnow(),
            appointment=self.appointment_170)

    def test_conc_med_required(self):
        medical_history = mommy.make_recipe(
            'esr21_subject.medicalhistory',
            subject_visit=self.visit
        )
        mommy.make_recipe(
            'esr21_subject.medicaldiagnosis',
            medical_history=medical_history,
            condition_related_meds=YES
        )
        medical_history.save()
        self.assertEqual(
            CrfMetadata.objects.get(
                model='esr21_subject.concomitantmedication',
                subject_identifier=self.consent.subject_identifier,
                visit_code='1170').entry_status, REQUIRED)

    def test_conc_med_not_required(self):
        medical_history = mommy.make_recipe(
            'esr21_subject.medicalhistory',
            subject_visit=self.visit
        )
        mommy.make_recipe(
            'esr21_subject.medicaldiagnosis',
            medical_history=medical_history,
            condition_related_meds=NO
        )
        medical_history.save()
        self.assertEqual(
            CrfMetadata.objects.get(
                model='esr21_subject.concomitantmedication',
                subject_identifier=self.consent.subject_identifier,
                visit_code='1170').entry_status, NOT_REQUIRED)
