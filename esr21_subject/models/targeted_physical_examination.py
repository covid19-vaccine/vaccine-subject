from django.db import models

from edc_base.model_managers import HistoricalRecords
from edc_base.model_validators import datetime_not_future
from edc_constants.choices import YES_NO, YES_NO_NA, NOT_APPLICABLE

from .model_mixins import CrfModelMixin
from ..choices import REASON_NOT_DRAWN


class TargetedPhysicalExamination(CrfModelMixin):

    physical_exam_performed = models.CharField(
        verbose_name='Was the physical examination performed?',
        max_length=35,
        choices=YES_NO)

    reason_not_done = models.CharField(
        verbose_name='If No, Reason Not Done',
        max_length=40,
        choices=REASON_NOT_DRAWN,
        blank=True,
        null=True,)

    area_performed = models.CharField(
        verbose_name='What area was the physical exam preformed?',
        max_length=35,
        blank=True,
        null=True,)

    exam_date = models.DateTimeField(
        verbose_name='Date of examination (DD MMM YYYY)',
        validators=[datetime_not_future, ],
        blank=True,
        null=True,)

    abnormalities = models.CharField(
        verbose_name='Were any abnormalities found?',
        max_length=30,
        default=NOT_APPLICABLE,
        choices=YES_NO_NA,
        help_text='Each clinically significant abnormal finding at screening'
                  ' will be recorded in the medical history')

    if_abnormalities = models.CharField(
        verbose_name='If Yes, were any abnormalities clinically significant? ',
        max_length=3,
        choices=YES_NO_NA,
        blank=True,
        null=True,)

    history = HistoricalRecords()

    class Meta(CrfModelMixin.Meta):
        app_label = 'esr21_subject'
        verbose_name = 'Targeted Physical Exam'
        verbose_name_plural = 'Targeted Physical Exam'
