from datetime import datetime
import arrow
from dateutil.tz import gettz
from django.apps import apps as django_apps

from edc_constants.constants import MALE, FEMALE, OTHER
from edc_consent.consent import Consent
from edc_consent.site_consents import site_consents


app_config = django_apps.get_app_config('edc_protocol')
edc_protocol = django_apps.get_app_config('edc_protocol')

tzinfo = gettz('Africa/Gaborone')

v1 = Consent(
    'esr21_subject.informedconsent',
    version='1',
    start=arrow.get(
        datetime(2021, 5, 1, 0, 0, 0), tzinfo=tzinfo).to('UTC').datetime,
    end=arrow.get(
        datetime(2022, 3, 14, 23, 59, 59), tzinfo=tzinfo).to('UTC').datetime,
    age_min=18,
    age_is_adult=18,
    age_max=160,
    gender=[MALE, FEMALE, OTHER])

v3 = Consent(
    'esr21_subject.informedconsent',
    version='3',
    start=arrow.get(
        datetime(2022, 3, 15, 0, 0, 0), tzinfo=tzinfo).to('UTC').datetime,
    end=arrow.get(
        datetime(2023, 12, 31, 23, 59, 59), tzinfo=tzinfo).to('UTC').datetime,
    age_min=18,
    age_is_adult=18,
    age_max=64,
    gender=[MALE, FEMALE, OTHER])

site_consents.register(v1)
site_consents.register(v3)
