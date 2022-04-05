from django.test import TestCase, tag
from edc_appointment.constants import COMPLETE_APPT
from edc_appointment.models import Appointment
from edc_base.utils import get_utcnow
from edc_constants.constants import YES, NO
from edc_facility.import_holidays import import_holidays
from edc_visit_tracking.constants import SCHEDULED
from model_mommy import mommy

from ..models import OnSchedule, OnScheduleIll, VaccinationHistory
from ..helper_classes import EnrollmentHelper
from dateutil.relativedelta import relativedelta


@tag('vs')
class TestVisitScheduleSetup(TestCase):

    databases = '__all__'

    def setUp(self):
        import_holidays()

        self.enrol_helper = EnrollmentHelper

        mommy.make_recipe(
            'esr21_subject.eligibilityconfirmation',)

        consent = mommy.make_recipe(
            'esr21_subject.informedconsent',
            subject_identifier='123-9876')

        mommy.make_recipe(
            'esr21_subject.screeningeligibility',
            subject_identifier=consent.subject_identifier,
            is_eligible=True)

        self.subject_identifier = consent.subject_identifier

        mommy.make_recipe(
            'esr21_subject.vaccinationhistory',
            subject_identifier=self.subject_identifier,
            received_vaccine=NO,
            dose_quantity=None)

    def test_onschedule_maincohort(self):
        """Assert that a participant is put onschedule for main study.
        """
        cohort = 'esr21'
        schedule_enrollment = self.enrol_helper(
            cohort=cohort, subject_identifier=self.subject_identifier)
        schedule_enrollment.schedule_enrol()

        self.assertEqual(OnSchedule.objects.filter(
            subject_identifier=self.subject_identifier,
            schedule_name='esr21_enrol_schedule3').count(), 1)

        self.assertEqual(OnSchedule.objects.filter(
            subject_identifier=self.subject_identifier,
            schedule_name='esr21_fu_schedule3').count(), 1)

        self.assertEqual(OnSchedule.objects.filter(
            subject_identifier=self.subject_identifier,
            schedule_name='esr21_boost_schedule').count(), 1)

    def test_consented_onschedule_subcohort(self):
        """Assert that a participant is put onschedule for subcohort.
        """
        eligibility = mommy.make_recipe(
            'esr21_subject.eligibilityconfirmation',)

        consent = mommy.make_recipe(
            'esr21_subject.informedconsent',
            screening_identifier=eligibility.screening_identifier,
            subject_identifier='123-9871')

        mommy.make_recipe(
            'esr21_subject.screeningeligibility',
            subject_identifier=consent.subject_identifier,
            is_eligible=True)

        mommy.make_recipe(
            'esr21_subject.vaccinationhistory',
            subject_identifier=consent.subject_identifier,
            received_vaccine=NO,
            dose_quantity=None)

        cohort = 'esr21_sub'
        schedule_enrollment = self.enrol_helper(
            cohort=cohort, subject_identifier=consent.subject_identifier)
        schedule_enrollment.schedule_enrol()

        self.assertEqual(OnSchedule.objects.filter(
            subject_identifier=consent.subject_identifier,
            schedule_name='esr21_sub_enrol_schedule3').count(), 1)

        self.assertEqual(OnSchedule.objects.filter(
            subject_identifier=consent.subject_identifier,
            schedule_name='esr21_sub_fu_schedule3').count(), 1)

        self.assertEqual(OnSchedule.objects.filter(
            subject_identifier=consent.subject_identifier,
            schedule_name='esr21_sub_boost_schedule').count(), 1)

    def test_maincohort_appts_created(self):
        """Assert that four appointments were created"""
        cohort = 'esr21'
        schedule_enrollment = self.enrol_helper(
            cohort=cohort, subject_identifier=self.subject_identifier)
        schedule_enrollment.schedule_enrol()

        self.assertEqual(Appointment.objects.filter(
            subject_identifier=self.subject_identifier,
            schedule_name='esr21_enrol_schedule3').count(), 2)

        self.assertEqual(Appointment.objects.get(
            subject_identifier=self.subject_identifier,
            schedule_name='esr21_enrol_schedule3',
            visit_code='1000').timepoint_datetime, get_utcnow().replace(microsecond=0))

        self.assertEqual(Appointment.objects.get(
            subject_identifier=self.subject_identifier,
            schedule_name='esr21_fu_schedule3',
            visit_code='1070').timepoint_datetime,
            (get_utcnow() + relativedelta(days=70)).replace(microsecond=0))

        self.assertEqual(Appointment.objects.get(
            subject_identifier=self.subject_identifier,
            schedule_name='esr21_fu_schedule3',
            visit_code='1070').timepoint_datetime,
            (get_utcnow() + relativedelta(days=70)).replace(microsecond=0))

#     @tag('vs1')
#     def test_illness_onschedule(self):
#         """Assert that a participant is put onschedule for illness visits if
#          they test positive for Covid 19.
#         """
# 
#         mommy.make_recipe(
#             'esr21_subject.eligibilityconfirmation',)
# 
#         consent = mommy.make_recipe(
#             'esr21_subject.informedconsent',
#             subject_identifier='123-9877')
# 
#         screening_eligibility = mommy.make_recipe(
#             'esr21_subject.screeningeligibility',
#             subject_identifier=consent.subject_identifier,
#             is_eligible=True)
# 
#         mommy.make_recipe(
#             'esr21_subject.subjectvisit',
#             appointment=Appointment.objects.get(visit_code='1000'),
#             report_datetime=get_utcnow(),
#             reason=SCHEDULED)
# 
#         visit = mommy.make_recipe(
#             'esr21_subject.subjectvisit',
#             appointment=Appointment.objects.get(visit_code='1007'),
#             report_datetime=get_utcnow(),
#             reason=SCHEDULED)
# 
#         mommy.make_recipe(
#             'esr21_subject.covid19symptomaticinfections',
#             subject_visit=visit,
#             symptomatic_experiences=YES)
# 
#         self.assertEqual(OnScheduleIll.objects.filter(
#             subject_identifier=screening_eligibility.subject_identifier,
#             schedule_name='esr21_illness_schedule').count(), 1)
# 
#     @tag('vs2')
#     def test_illness_not_onschedule(self):
#         """Assert that a participant is not put onschedule for illness visits if
#          they test positive for Covid 19 and they are already on an illness schedule.
#         """
# 
#         mommy.make_recipe(
#             'esr21_subject.eligibilityconfirmation',)
# 
#         consent = mommy.make_recipe(
#             'esr21_subject.informedconsent',
#             subject_identifier='123-9877')
# 
#         screening_eligibility = mommy.make_recipe(
#             'esr21_subject.screeningeligibility',
#             subject_identifier=consent.subject_identifier,
#             is_eligible=True)
# 
#         mommy.make_recipe(
#             'esr21_subject.subjectvisit',
#             appointment=Appointment.objects.get(visit_code='1000'),
#             report_datetime=get_utcnow(),
#             reason=SCHEDULED)
# 
#         visit1 = mommy.make_recipe(
#             'esr21_subject.subjectvisit',
#             appointment=Appointment.objects.get(visit_code='1007'),
#             report_datetime=get_utcnow(),
#             reason=SCHEDULED)
# 
#         mommy.make_recipe(
#             'esr21_subject.covid19symptomaticinfections',
#             subject_visit=visit1,
#             symptomatic_experiences=YES)
# 
#         self.assertEqual(OnScheduleIll.objects.filter(
#             subject_identifier=screening_eligibility.subject_identifier,
#             schedule_name='esr21_illness_schedule').count(), 1)
# 
#         visit2 = mommy.make_recipe(
#             'esr21_subject.subjectvisit',
#             appointment=Appointment.objects.get(visit_code='1014'),
#             report_datetime=get_utcnow(),
#             reason=SCHEDULED)
# 
#         mommy.make_recipe(
#             'esr21_subject.covid19symptomaticinfections',
#             subject_visit=visit2,
#             symptomatic_experiences=YES)
# 
#         self.assertEqual(OnScheduleIll.objects.filter(
#             subject_identifier=screening_eligibility.subject_identifier,
#             schedule_name='esr21_illness1_schedule').count(), 0)
# 
#     @tag('vs3')
#     def test_illness2_onschedule(self):
#         """Assert that a participant is put onschedule for second illness visits if
#          they test positive for Covid 19 for the second time.
#         """
# 
#         mommy.make_recipe(
#             'esr21_subject.eligibilityconfirmation',)
# 
#         consent = mommy.make_recipe(
#             'esr21_subject.informedconsent',
#             subject_identifier='123-9877')
# 
#         screening_eligibility = mommy.make_recipe(
#             'esr21_subject.screeningeligibility',
#             subject_identifier=consent.subject_identifier,
#             is_eligible=True)
# 
#         mommy.make_recipe(
#             'esr21_subject.subjectvisit',
#             appointment=Appointment.objects.get(
#                 visit_code='1000',
#                 subject_identifier=screening_eligibility.subject_identifier),
#             report_datetime=get_utcnow(),
#             reason=SCHEDULED)
# 
#         visit1 = mommy.make_recipe(
#             'esr21_subject.subjectvisit',
#             appointment=Appointment.objects.get(
#                 visit_code='1007',
#                 subject_identifier=screening_eligibility.subject_identifier),
#             report_datetime=get_utcnow(),
#             reason=SCHEDULED)
# 
#         mommy.make_recipe(
#             'esr21_subject.covid19symptomaticinfections',
#             subject_visit=visit1,
#             symptomatic_experiences=YES)
# 
#         self.assertEqual(OnScheduleIll.objects.filter(
#             subject_identifier=screening_eligibility.subject_identifier,
#             schedule_name='esr21_illness_schedule').count(), 1)
# 
#         appt = Appointment.objects.get(
#                 visit_code='2028',
#                 subject_identifier=screening_eligibility.subject_identifier)
# 
#         appt.appt_status = COMPLETE_APPT
#         appt.save()
# 
#         # mommy.make_recipe(
#             # 'esr21_subject.offscheduleill',
#             # subject_identifier=informed_consent.subject_identifier)
# 
#         visit2 = mommy.make_recipe(
#             'esr21_subject.subjectvisit',
#             appointment=Appointment.objects.get(visit_code='1014'),
#             report_datetime=get_utcnow(),
#             reason=SCHEDULED)
# 
#         mommy.make_recipe(
#             'esr21_subject.covid19symptomaticinfections',
#             subject_visit=visit2,
#             symptomatic_experiences=YES)
# 
#         self.assertEqual(OnScheduleIll.objects.filter(
#             subject_identifier=screening_eligibility.subject_identifier,
#             schedule_name='esr21_illness2_schedule').count(), 1)
# 
#     @tag('vs3')
#     def test_illness2_onschedule_invalid(self):
#         """Assert that a participant is not put onschedule for second illness visit
#         """
# 
#         mommy.make_recipe(
#             'esr21_subject.eligibilityconfirmation',)
# 
#         consent = mommy.make_recipe(
#             'esr21_subject.informedconsent',
#             subject_identifier='123-9877')
# 
#         screening_eligibility = mommy.make_recipe(
#             'esr21_subject.screeningeligibility',
#             subject_identifier=consent.subject_identifier,
#             is_eligible=True)
# 
#         mommy.make_recipe(
#             'esr21_subject.subjectvisit',
#             appointment=Appointment.objects.get(
#                 visit_code='1000',
#                 subject_identifier=screening_eligibility.subject_identifier),
#             report_datetime=get_utcnow(),
#             reason=SCHEDULED)
# 
#         visit1 = mommy.make_recipe(
#             'esr21_subject.subjectvisit',
#             appointment=Appointment.objects.get(
#                 visit_code='1007',
#                 subject_identifier=screening_eligibility.subject_identifier),
#             report_datetime=get_utcnow(),
#             reason=SCHEDULED)
# 
#         mommy.make_recipe(
#             'esr21_subject.covid19symptomaticinfections',
#             subject_visit=visit1,
#             symptomatic_experiences=YES)
# 
#         visit2 = mommy.make_recipe(
#             'esr21_subject.subjectvisit',
#             appointment=Appointment.objects.get(
#                 visit_code='1014',
#                 subject_identifier=screening_eligibility.subject_identifier),
#             report_datetime=get_utcnow(),
#             reason=SCHEDULED)
# 
#         mommy.make_recipe(
#             'esr21_subject.covid19symptomaticinfections',
#             subject_visit=visit2,
#             symptomatic_experiences=YES)
# 
#         self.assertEqual(OnScheduleIll.objects.filter(
#             subject_identifier=screening_eligibility.subject_identifier,
#             schedule_name='esr21_illness_schedule').count(), 1)
# 
#         self.assertNotEqual(OnScheduleIll.objects.filter(
#             subject_identifier=screening_eligibility.subject_identifier,
#             schedule_name='esr21_illness2_schedule').count(), 1)
