from django.db import models
from edc_base.model_fields import OtherCharField
from edc_base.model_validators.date import date_not_future, date_is_future
from edc_constants.choices import YES_NO, YES_NO_NA
from edc_constants.constants import NO, YES

from ..choices import YES_NO_OTHER
from .list_models import Contraception
from .model_mixins import CrfModelMixin


class PregnancyStatus(CrfModelMixin):

    primary_amenorrhea = models.CharField(
        verbose_name='Does the participant have primary amenorrhea?',
        choices=YES_NO,
        max_length=3,)

    start_date_menstrual_period = models.DateField(
        verbose_name='Start Date of Last Menstrual Period (DD/MMM/YYYY)',
        validators=[date_not_future, ],
        null=True,
        blank=True)

    expected_delivery = models.DateField(
        verbose_name='Date of Expected Delivery (DD/MMM/YYYY)',
        validators=[date_is_future, ],
        null=True,
        blank=True)

    contraceptive_usage = models.CharField(
        verbose_name='Using Contraception',
        choices=YES_NO_NA,
        max_length=3,)

    contraceptive = models.ManyToManyField(
        Contraception,
        verbose_name='If yes, specify contraception',
        max_length=30,
        blank=True,)

    contraceptive_other = OtherCharField()

    """""Childbearing Potential"""""

    surgically_sterilized = models.CharField(
        verbose_name='Is the participant considered to be surgically sterilized?',
        choices=YES_NO,
        max_length=3)

    amenorrhea_history = models.CharField(
        verbose_name=('Does the participant have a history of >= 12 months amenorrhea prior'
                      ' to randomization, without an alternative cause, following cessation'
                      ' of exogenous sex-hormonal treatment?'),
        choices=YES_NO,
        max_length=3,
        help_text='Including bilateral tubal ligation, bilateral oophorectomy,or hysterectomy')

    post_menopausal_range = models.CharField(
        verbose_name=('Does the participant have a follicle-stimulating hormone level in the'
                      ' post-menopausal range?'),
        choices=YES_NO,
        max_length=12,
        help_text=('Until follicle-stimulating hormone is documented to be within menopausal'
                   ' range, the participant is to be considered of childbearing potential.')
        )

    post_menopausal = models.CharField(
        verbose_name='Is the woman considered to be post-menopausal?',
        choices=YES_NO_OTHER,
        max_length=10)

    post_menopausal_other = models.TextField(
        verbose_name='If other, specify',
        max_length=150,
        null=True,
        blank=True)

    comment = models.TextField(
        verbose_name='Comment',
        max_length=200,
        null=True,
        blank=True)

    child_bearing_potential = models.CharField(
        max_length=3,
        choices=YES_NO,
        blank=True)

    """""Pregnancy History"""""

    number_prev_pregnancies = models.PositiveIntegerField(
        verbose_name='Overall number of previous pregnancies',
        null=True,
        blank=True)

    number_normal_pregnancies = models.PositiveIntegerField(
        verbose_name='Number of normal deliveries',
        null=True,
        blank=True)

    number_miscarriages = models.PositiveIntegerField(
        verbose_name='Number of spontaneous miscarriages',
        null=True,
        blank=True)

    date_miscarriages = models.DateField(
        verbose_name='Date of last spontaneous miscarriage',
        validators=[date_not_future, ],
        null=True,
        blank=True)

    risk_factor = models.CharField(
        verbose_name='Relevant pregnancy risk factor',
        max_length=10,
        null=True,
        blank=True)

    def save(self, *args, **kwargs):

        if self.post_menopausal == NO and self.surgically_sterilized == NO:
            self.child_bearing_potential = YES
        else:
            self.child_bearing_potential = NO

        super().save(*args, **kwargs)

    class Meta(CrfModelMixin.Meta):
        app_label = 'esr21_subject'
        verbose_name = 'Pregnancy Status'
        verbose_name_plural = 'Pregnancy Status'
