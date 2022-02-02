from django.db import models
from edc_constants.choices import POS_NEG
from .model_mixins import CrfModelMixin


class Covid19Results(CrfModelMixin):

    covid_result = models.CharField(
        verbose_name="What was your covid 19 result?",
        choices=POS_NEG,
        max_length=15,
        null=True,
        blank=True)

    class Meta(CrfModelMixin.Meta):
        app_label = 'esr21_subject'
        verbose_name = 'Covid19 Results'
        verbose_name_plural = 'Covid19 Results'
