from django.db import models
from edc_base.model_managers import HistoricalRecords
from edc_constants.choices import YES_NO

from .model_mixins import CrfModelMixin
from ..choices import TEST_TYPE


class SampleCollection(CrfModelMixin):

    sample_collected = models.CharField(
        verbose_name='Sample collection:',
        choices=YES_NO,
        max_length=3)

    date_collected = models.DateField(
        verbose_name='Sample collection Date:',
        blank=True,
        null=True)

    test_type = models.CharField(
        verbose_name='Test performed',
        choices=TEST_TYPE,
        max_length=20)

    test_type_other = models.CharField(
        verbose_name='Other ,specify',
        max_length=50,
        blank=True,
        null=True)

    history = HistoricalRecords()

    class Meta(CrfModelMixin.Meta):
        app_label = 'esr21_subject'
        verbose_name = 'Sample Collection'
        verbose_name_plural = 'Sample Collection'
