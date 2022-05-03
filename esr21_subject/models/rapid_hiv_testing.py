from django.db import models
from edc_base.model_managers import HistoricalRecords
from edc_base.model_validators import date_not_future
from edc_constants.choices import YES_NO, POS_NEG, YES_NO_NA
from edc_protocol.validators import date_not_before_study_start

from .model_mixins import CrfModelMixin
from ..choices import POS_NEG_IND


class RapidHIVTesting(CrfModelMixin):

    hiv_testing_consent = models.CharField(
        verbose_name='Do you consent to having HIV testing?',
        choices=YES_NO,
        max_length=3,)

    prev_hiv_test = models.CharField(
        verbose_name=(
            "Have you tested for HIV before?"),
        choices=YES_NO_NA,
        max_length=3)

    evidence_hiv_status = models.CharField(
        verbose_name="(Interviewer) Have you seen evidence of the HIV result?",
        max_length=15,
        null=True,
        blank=False,
        choices=YES_NO_NA,
        help_text=(
            "evidence = clinic and/or IDCC records. check regimes/drugs. "))

    hiv_test_date = models.DateField(
        verbose_name="Date of HIV Test",
        validators=[date_not_future, ],
        blank=True,
        null=True)

    hiv_result = models.CharField(
        verbose_name="What was your result?",
        choices=POS_NEG,
        max_length=15,
        null=True,
        blank=True)

    rapid_test_done = models.CharField(
        verbose_name='Was a rapid test processed?',
        choices=YES_NO_NA,
        max_length=3)

    rapid_test_date = models.DateField(
        validators=[
            date_not_before_study_start,
            date_not_future, ],
        verbose_name='Date of rapid test',
        blank=True,
        null=True)

    rapid_test_result = models.CharField(
        verbose_name='What is the rapid test result?',
        choices=POS_NEG_IND,
        max_length=15,
        blank=True,
        null=True)

    comments = models.TextField(
        verbose_name='Comment',
        max_length=250,
        blank=True,
        null=True)

    history = HistoricalRecords()

    class Meta(CrfModelMixin.Meta):
        app_label = 'esr21_subject'
        verbose_name = 'Rapid HIV Testing'
        verbose_name_plural = 'Rapid HIV Testing'
