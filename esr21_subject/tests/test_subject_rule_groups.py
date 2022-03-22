from dateutil.relativedelta import relativedelta
from django.test import TestCase, tag
from edc_appointment.models import Appointment
from edc_base.utils import get_utcnow
from edc_constants.constants import OMANG, FEMALE, MALE, NO, YES, NEG, POS
from edc_facility.import_holidays import import_holidays
from edc_metadata.constants import REQUIRED, NOT_REQUIRED
from edc_metadata.models import CrfMetadata, RequisitionMetadata
from edc_visit_schedule.site_visit_schedules import site_visit_schedules
from edc_visit_tracking.constants import SCHEDULED, UNSCHEDULED
from model_mommy import mommy

from ..models import ScreeningEligibility


@tag('rg')
class TestRuleGroups(TestCase):

    def setUp(self):
        import_holidays()

        self.eligibility = mommy.make_recipe(
            'esr21_subject.eligibilityconfirmation')

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

        self.subject_consent = mommy.make_recipe(
            'esr21_subject.informedconsent',
            **self.consent_options)

        mommy.make_recipe(
            'esr21_subject.screeningeligibility',
            subject_identifier=self.subject_consent.subject_identifier)

        self.subject_identifier = self.subject_consent.subject_identifier

        screening_eligibility = ScreeningEligibility.objects.get(
            subject_identifier=self.subject_identifier)

        if screening_eligibility.is_eligible:
            cohort = 'esr21'
            onschedule_model = 'esr21_subject.onschedule'

            self.put_on_schedule(f'{cohort}_enrol_schedule',
                                 onschedule_model=onschedule_model,
                                 subject_identifier=self.subject_identifier,
                                 onschedule_datetime=screening_eligibility.created.replace(microsecond=0))

            self.put_on_schedule(f'{cohort}_fu_schedule',
                                 onschedule_model=onschedule_model,
                                 subject_identifier=self.subject_identifier,
                                 onschedule_datetime=screening_eligibility.created.replace(microsecond=0))

            self.subject_visit = mommy.make_recipe(
                'esr21_subject.subjectvisit',
                appointment=Appointment.objects.get(
                    visit_code='1000',
                    subject_identifier=self.subject_consent.subject_identifier),
                report_datetime=get_utcnow(),
                reason=SCHEDULED)

    def test_pregnancy_form_required(self):
        self.assertEqual(
            CrfMetadata.objects.get(
                model='esr21_subject.pregnancystatus',
                subject_identifier=self.subject_identifier,
                visit_code='1000',
                visit_code_sequence=0).entry_status, REQUIRED)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='esr21_subject.pregnancytest',
                subject_identifier=self.subject_identifier,
                visit_code='1000',
                visit_code_sequence=0).entry_status, NOT_REQUIRED)

    def test_pregnancy_form_required_1070(self):

        mommy.make_recipe(
                'esr21_subject.subjectvisit',
                appointment=Appointment.objects.get(visit_code='1007'),
                report_datetime=get_utcnow(),
                reason=SCHEDULED)

        mommy.make_recipe(
                'esr21_subject.subjectvisit',
                appointment=Appointment.objects.get(visit_code='1014'),
                report_datetime=get_utcnow(),
                reason=SCHEDULED)

        mommy.make_recipe(
                'esr21_subject.subjectvisit',
                appointment=Appointment.objects.get(visit_code='1028'),
                report_datetime=get_utcnow(),
                reason=SCHEDULED)

        mommy.make_recipe(
                'esr21_subject.subjectvisit',
                appointment=Appointment.objects.get(visit_code='1070'),
                report_datetime=get_utcnow(),
                reason=SCHEDULED)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='esr21_subject.pregnancystatus',
                subject_identifier=self.subject_identifier,
                visit_code='1070',
                visit_code_sequence=0).entry_status, REQUIRED)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='esr21_subject.pregnancytest',
                subject_identifier=self.subject_identifier,
                visit_code='1070',
                visit_code_sequence=0).entry_status, NOT_REQUIRED)

    def test_pregnancy_status_form_not_required(self):

        eligibility = mommy.make_recipe(
            'esr21_subject.eligibilityconfirmation')

        consent_options = {
            'screening_identifier': eligibility.screening_identifier,
            'consent_datetime': get_utcnow(),
            'version': 1,
            'dob': (get_utcnow() - relativedelta(years=45)).date(),
            'first_name': 'JOHN',
            'last_name': 'DOE',
            'initials': 'JD',
            'identity': '123415678',
            'confirm_identity': '123415678',
            'identity_type': OMANG,
            'gender': MALE}

        subject_consent = mommy.make_recipe(
            'esr21_subject.informedconsent',
            **consent_options)

        mommy.make_recipe(
            'esr21_subject.screeningeligibility',
            subject_identifier=subject_consent.subject_identifier)

        screening_eligibility = ScreeningEligibility.objects.get(
            subject_identifier=subject_consent.subject_identifier)

        if screening_eligibility.is_eligible:
            cohort = 'esr21'
            onschedule_model = 'esr21_subject.onschedule'

            self.put_on_schedule(f'{cohort}_enrol_schedule',
                                 onschedule_model=onschedule_model,
                                 subject_identifier=subject_consent.subject_identifier,
                                 onschedule_datetime=screening_eligibility.created.replace(microsecond=0))

            self.put_on_schedule(f'{cohort}_fu_schedule',
                                 onschedule_model=onschedule_model,
                                 subject_identifier=subject_consent.subject_identifier,
                                 onschedule_datetime=screening_eligibility.created.replace(microsecond=0))

        mommy.make_recipe(
            'esr21_subject.subjectvisit',
            appointment=Appointment.objects.get(
                visit_code='1000',
                subject_identifier=subject_consent.subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='esr21_subject.pregnancystatus',
                subject_identifier=subject_consent.subject_identifier,
                visit_code='1000',
                visit_code_sequence=0).entry_status, NOT_REQUIRED)

    def test_pregnancy_test_not_required(self):
        """
        Assert Pregnancy test form not required if female and not of childbearing
        potential on the pregnancy status form.
        """
        mommy.make_recipe(
            'esr21_subject.pregnancystatus',
            subject_visit=self.subject_visit,
            post_menopausal=YES,
            surgically_sterilized=NO)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='esr21_subject.pregnancytest',
                subject_identifier=self.subject_identifier,
                visit_code='1000',
                visit_code_sequence=0).entry_status, NOT_REQUIRED)

    def test_pregnancy_test_required(self):
        self.consent_options['dob'] = (get_utcnow() - relativedelta(years=55)).date()
        self.consent_options['identity'] = '111125678'
        self.consent_options['confirm_identity'] = '111125678'

        subject_consent = mommy.make_recipe(
            'esr21_subject.informedconsent',
            **self.consent_options)

        mommy.make_recipe(
            'esr21_subject.screeningeligibility',
            subject_identifier=subject_consent.subject_identifier)

        screening_eligibility = ScreeningEligibility.objects.get(
            subject_identifier=subject_consent.subject_identifier)

        if screening_eligibility.is_eligible:
            cohort = 'esr21'
            onschedule_model = 'esr21_subject.onschedule'

            self.put_on_schedule(f'{cohort}_enrol_schedule',
                                 onschedule_model=onschedule_model,
                                 subject_identifier=subject_consent.subject_identifier,
                                 onschedule_datetime=screening_eligibility.created.replace(microsecond=0))

            self.put_on_schedule(f'{cohort}_fu_schedule',
                                 onschedule_model=onschedule_model,
                                 subject_identifier=subject_consent.subject_identifier,
                                 onschedule_datetime=screening_eligibility.created.replace(microsecond=0))

        subject_visit = mommy.make_recipe(
            'esr21_subject.subjectvisit',
            appointment=Appointment.objects.get(
                visit_code='1000',
                subject_identifier=subject_consent.subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        mommy.make_recipe(
            'esr21_subject.pregnancystatus',
            subject_visit=subject_visit,
            post_menopausal=NO,
            surgically_sterilized=NO)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='esr21_subject.pregnancytest',
                subject_identifier=subject_consent.subject_identifier,
                visit_code='1000',
                visit_code_sequence=0).entry_status, REQUIRED)

    def test_pregnancy_status_required_fu(self):

        mommy.make_recipe(
            'esr21_subject.subjectvisit',
            appointment=Appointment.objects.get(visit_code='1007'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='esr21_subject.pregnancystatus',
                subject_identifier=self.subject_identifier,
                visit_code='1007',
                visit_code_sequence=0).entry_status, REQUIRED)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='esr21_subject.pregnancytest',
                subject_identifier=self.subject_identifier,
                visit_code='1007',
                visit_code_sequence=0).entry_status, NOT_REQUIRED)

    def test_pregnancy_test_not_required_fu(self):

        subject_visit = mommy.make_recipe(
            'esr21_subject.subjectvisit',
            appointment=Appointment.objects.get(visit_code='1007'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        mommy.make_recipe(
            'esr21_subject.pregnancystatus',
            subject_visit=subject_visit,
            post_menopausal=NO,
            surgically_sterilized=NO)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='esr21_subject.pregnancytest',
                subject_identifier=self.subject_identifier,
                visit_code='1007',
                visit_code_sequence=0).entry_status, NOT_REQUIRED)

    def test_pregnancy_not_required_unscheduled(self):
        """
        Assert pregnancy form not required for unscheduled visits, for female
        participant.
        """
        appt_1000_1 = Appointment.objects.create(
            appt_datetime=get_utcnow(),
            subject_identifier=self.subject_identifier,
            visit_schedule_name='esr21_visit_schedule',
            schedule_name='esr21_enrol_schedule',
            visit_code='1000',
            visit_code_sequence=1)

        mommy.make_recipe(
            'esr21_subject.subjectvisit',
            appointment=appt_1000_1,
            report_datetime=get_utcnow(),
            reason=UNSCHEDULED)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='esr21_subject.pregnancystatus',
                subject_identifier=self.subject_identifier,
                visit_code='1000',
                visit_code_sequence=1).entry_status, NOT_REQUIRED)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='esr21_subject.pregnancytest',
                subject_identifier=self.subject_identifier,
                visit_code='1000',
                visit_code_sequence=1).entry_status, NOT_REQUIRED)

    def test_vaccination_if_symptomatic(self):
        """
        Assert Vaccination Details and Physical Exam form not required if participant
        enrolled has covid-like symptoms
        """
        self.assertEqual(
            CrfMetadata.objects.get(
                model='esr21_subject.physicalexam',
                subject_identifier=self.subject_identifier,
                visit_code='1000',
                visit_code_sequence=0).entry_status, NOT_REQUIRED)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='esr21_subject.vaccinationdetails',
                subject_identifier=self.subject_identifier,
                visit_code='1000',
                visit_code_sequence=0).entry_status, NOT_REQUIRED)

        # Assert SARS-CoV-2 requisition is required.
        self.assertEqual(
            RequisitionMetadata.objects.get(
                model='esr21_subject.subjectrequisition',
                panel_name='sars_cov2_pcr',
                subject_identifier=self.subject_identifier,
                visit_code='1000',
                visit_code_sequence=0).entry_status, REQUIRED)

    def test_vaccination_covid19_results_neg(self):
        """
        Assert Vaccination Details and Physical Exam form required if participant
        enrolled has covid-like symptoms, but with negative covid test results.
        """
        mommy.make_recipe(
            'esr21_subject.covid19results',
            subject_visit=self.subject_visit,
            covid_result=NEG)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='esr21_subject.physicalexam',
                subject_identifier=self.subject_identifier,
                visit_code='1000',
                visit_code_sequence=0).entry_status, REQUIRED)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='esr21_subject.vaccinationdetails',
                subject_identifier=self.subject_identifier,
                visit_code='1000',
                visit_code_sequence=0).entry_status, REQUIRED)

    def test_vaccination_codvid19_results_pos(self):
        """
        Assert Vaccination Details and Physical Exam form required if participant
        enrolled has covid-like symptoms, but with positive covid test results.
        """
        mommy.make_recipe(
            'esr21_subject.covid19results',
            subject_visit=self.subject_visit,
            covid_result=POS)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='esr21_subject.physicalexam',
                subject_identifier=self.subject_identifier,
                visit_code='1000',
                visit_code_sequence=0).entry_status, NOT_REQUIRED)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='esr21_subject.vaccinationdetails',
                subject_identifier=self.subject_identifier,
                visit_code='1000',
                visit_code_sequence=0).entry_status, NOT_REQUIRED)

        # Assert SARS-CoV-2 requisition is required.
        self.assertEqual(
            RequisitionMetadata.objects.get(
                model='esr21_subject.subjectrequisition',
                panel_name='sars_cov2_pcr',
                subject_identifier=self.subject_identifier,
                visit_code='1000',
                visit_code_sequence=0).entry_status, REQUIRED)

    def test_vaccination_if_not_symptomatic(self):
        """
        Assert Vaccination Details and Physical Exam form required if participant
        enrolled doesn't have covid-like symptoms
        """
        screening_eligibility = ScreeningEligibility.objects.get(
            subject_identifier=self.subject_identifier)

        screening_eligibility.symptomatic_infections_experiences = NO

        screening_eligibility.save()

        self.subject_visit.save()

        self.assertEqual(
            CrfMetadata.objects.get(
                model='esr21_subject.physicalexam',
                subject_identifier=self.subject_identifier,
                visit_code='1000',
                visit_code_sequence=0).entry_status, REQUIRED)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='esr21_subject.vaccinationdetails',
                subject_identifier=self.subject_identifier,
                visit_code='1000',
                visit_code_sequence=0).entry_status, REQUIRED)

        # Assert SARS-CoV-2 requisition is not required.
        self.assertEqual(
            RequisitionMetadata.objects.get(
                model='esr21_subject.subjectrequisition',
                panel_name='sars_cov2_pcr',
                subject_identifier=self.subject_identifier,
                visit_code='1000',
                visit_code_sequence=0).entry_status, NOT_REQUIRED)

    @tag('vf')
    def test_vaccination_not_required_fu(self):
        """
        Assert Vaccination details and physical exam form not required on follow
        up visits, and unscheduled.
        """
        # Update participant 'No' symptomatic
        screening_eligibility = ScreeningEligibility.objects.get(
            subject_identifier=self.subject_identifier)

        screening_eligibility.symptomatic_infections_experiences = NO

        screening_eligibility.save()

        # Follow up visit
        mommy.make_recipe(
            'esr21_subject.subjectvisit',
            appointment=Appointment.objects.get(visit_code='1007'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='esr21_subject.physicalexam',
                subject_identifier=self.subject_identifier,
                visit_code='1007',
                visit_code_sequence=0).entry_status, NOT_REQUIRED)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='esr21_subject.vaccinationdetails',
                subject_identifier=self.subject_identifier,
                visit_code='1007',
                visit_code_sequence=0).entry_status, NOT_REQUIRED)

        # Unschedule visit
        appt_1007_1 = Appointment.objects.create(
            appt_datetime=get_utcnow(),
            subject_identifier=self.subject_identifier,
            visit_schedule_name='esr21_visit_schedule',
            schedule_name='esr21_fu_schedule',
            visit_code='1007',
            visit_code_sequence=1)

        mommy.make_recipe(
            'esr21_subject.subjectvisit',
            appointment=appt_1007_1,
            report_datetime=get_utcnow(),
            reason=UNSCHEDULED)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='esr21_subject.physicalexam',
                subject_identifier=self.subject_identifier,
                visit_code='1007',
                visit_code_sequence=1).entry_status, NOT_REQUIRED)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='esr21_subject.vaccinationdetails',
                subject_identifier=self.subject_identifier,
                visit_code='1007',
                visit_code_sequence=1).entry_status, NOT_REQUIRED)

    def put_on_schedule(self, schedule_name, onschedule_model, subject_identifier,
                        onschedule_datetime=None):
        _, schedule = site_visit_schedules.get_by_onschedule_model_schedule_name(
            onschedule_model=onschedule_model, name=schedule_name)
        schedule.put_on_schedule(
            subject_identifier=subject_identifier,
            onschedule_datetime=onschedule_datetime,
            schedule_name=schedule_name)
