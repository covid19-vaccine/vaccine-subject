from django.db import models
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators import date_not_future
from edc_base.sites import SiteModelMixin
from edc_constants.choices import YES_NO_NOT_EVALUATED
from edc_protocol.validators import date_not_before_study_start

from .model_mixins.crf_model_mixin import CrfModelMixin
from ..choices import PREG_OUTCOMES, BIRTH_METHODS


class PregOutcome(CrfModelMixin):

    outcome_count = models.IntegerField(
        verbose_name='How many outcomes resulted from the reported pregnancy', )

    comments = models.TextField(
        verbose_name='Comments',
        blank=True,
        null=True,)

    history = HistoricalRecords()

    class Meta(CrfModelMixin.Meta):
        verbose_name = 'Pregnancy Outcome'
        app_label = 'esr21_subject'


class OutcomeManager(models.Manager):

    def get_by_natural_key(self, outcome_date, specify_outcome):
        return self.get(outcome_date=outcome_date,
                        specify_outcome=specify_outcome)


class OutcomeInline(SiteModelMixin, BaseUuidModel):
    preg_outcome = models.ForeignKey(
        PregOutcome,
        on_delete=models.PROTECT)

    outcome_date = models.DateField(
        verbose_name='Outcome Date',
        validators=[
            date_not_before_study_start,
            date_not_future, ])

    specify_outcome = models.CharField(
        verbose_name='Specify outcome',
        max_length=30,
        choices=PREG_OUTCOMES,
    )

    method = models.CharField(
        verbose_name='Method',
        blank=True,
        null=True,
        max_length=30,
        choices=BIRTH_METHODS,
    )

    infant_anomalies = models.CharField(
        verbose_name='Were any fetal/Infant congenital anomalies identified',
        help_text='If yes, complete the AE log.',
        max_length=30,
        choices=YES_NO_NOT_EVALUATED,)

    objects = OutcomeManager()

    history = HistoricalRecords()

    def natural_key(self):
        return (self.outcome_date, self.specify_outcome,) + self.preg_outcome.natural_key()

    natural_key.dependencies = ['esr21_subject.pregoutcome']

    class Meta:
        verbose_name = 'Pregnancy Outcome Inline'
        app_label = 'esr21_subject'
