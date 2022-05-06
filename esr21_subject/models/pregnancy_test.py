from django.db import models
from edc_constants.choices import POS_NEG, YES_NO
from edc_base.model_managers import HistoricalRecords
from edc_base.model_validators.date import datetime_not_future

from .model_mixins import CrfModelMixin
from ..choices import PREGNANCY_TEST_TYPE


class PregnancyTest(CrfModelMixin):

    preg_performed = models.CharField(
        verbose_name='Was the pregnancy test performed?',
        max_length=20,
        choices=YES_NO,)

    preg_test_type = models.CharField(
        verbose_name='Type of pregnancy test performed',
        max_length=30,
        choices=PREGNANCY_TEST_TYPE,
        null=True,
        blank=True,)

    preg_date = models.DateTimeField(
        verbose_name='Date of pregnancy test',
        validators=[datetime_not_future, ],
        help_text=' (DD MMM YYYY)',
        null=True,
        blank=True)

    result = models.CharField(
        verbose_name='Result',
        choices=POS_NEG,
        max_length=20,
        null=True,
        blank=True)

    history = HistoricalRecords()

    class Meta(CrfModelMixin.Meta):
        verbose_name = 'Pregnancy Test'
        verbose_name_plural = 'Pregnancy Test'
