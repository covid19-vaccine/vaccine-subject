from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from edc_base.model_managers import HistoricalRecords
from edc_base.model_validators.date import datetime_not_future
from edc_constants.choices import YES_NO
from edc_constants.constants import NOT_APPLICABLE
from .model_mixins import CrfModelMixin
from ..choices import REASON, TEMP_UNITS


class VitalSigns(CrfModelMixin):
    vital_signs_measured = models.CharField(
        verbose_name='Were the vital signs measurements performed?',
        max_length=3,
        choices=YES_NO)

    reason_vitals_nd = models.CharField(
        verbose_name='If No, Reason Not Done',
        max_length=30,
        choices=REASON,
        default=NOT_APPLICABLE)

    assessment_dt = models.DateTimeField(
        verbose_name='Date and Time of Assessment',
        validators=[datetime_not_future],
        blank=True,
        null=True)

    systolic_bp = models.PositiveIntegerField(
        verbose_name='Systolic Blood Pressure',
        help_text='Fixed Unit: mmHg',
        validators=[MinValueValidator(75), MaxValueValidator(220), ],
        blank=True,
        null=True)

    diastolic_bp = models.PositiveIntegerField(
        verbose_name='Diastolic Blood Pressure',
        help_text='Fixed Unit: mmHg',
        validators=[MinValueValidator(55), MaxValueValidator(150), ],
        blank=True,
        null=True)

    heart_rate = models.PositiveIntegerField(
        verbose_name='Heart Rate',
        help_text='beats/min',
        blank=True,
        null=True)

    body_temp = models.DecimalField(
        verbose_name='Body Temperature',
        max_digits=5,
        decimal_places=2,
        validators=[
            MinValueValidator(
                30, message="Cannot below 30"),
            MaxValueValidator(
                60, message="Cannot be above 60"), ],
        blank=True,
        null=True)

    body_temp_unit = models.CharField(
        verbose_name='Unit of temperature',
        choices=TEMP_UNITS,
        max_length=15, )

    oxygen_saturated = models.DecimalField(
        verbose_name='Oxygen Saturation (via Pulse Oximetry)',
        validators=[MinValueValidator(0), ],
        max_digits=5,
        decimal_places=2,
        help_text='Fixed Unit: %',
        null=True,
        blank=True)

    comment = models.TextField(
        verbose_name='Comment',
        blank=True,
        null=True)

    history = HistoricalRecords()

    class Meta(CrfModelMixin.Meta):
        app_label = 'esr21_subject'
        verbose_name = 'Vital signs'
        verbose_name_plural = 'Vital signs'
