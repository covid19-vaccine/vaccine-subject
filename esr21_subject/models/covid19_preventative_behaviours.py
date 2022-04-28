from django.db import models

from .model_mixins import CrfModelMixin
from ..choices import AGREE_DISAGREE


class Covid19PreventativeBehaviours(CrfModelMixin):

    people_sneezing = models.CharField(
        verbose_name='It really bothers me when people sneeze '
                     'without covering their mouths',
        max_length=20,
        choices=AGREE_DISAGREE)

    avoid_touching = models.CharField(
        verbose_name='I avoid touching door handles and staircase railing at '
                     'public locations',
        max_length=20,
        choices=AGREE_DISAGREE)

    dislike_face_mask = models.CharField(
        verbose_name='I dislike wearing face mask because of the way it '
                     'looks and/or feels',
        max_length=20,
        choices=AGREE_DISAGREE)

    temperature = models.CharField(
        verbose_name='I want people\'s temperature to be taken before they '
                     'enter public places',
        max_length=20,
        choices=AGREE_DISAGREE)

    crowded_places = models.CharField(
        verbose_name='I dont mind going to very crowded places',
        max_length=20,
        choices=AGREE_DISAGREE)

    self_isolate = models.CharField(
        verbose_name='I would self-isolate myself at home if needed',
        max_length=20,
        choices=AGREE_DISAGREE)

    use_hand_sanitizer = models.CharField(
        verbose_name='I frequently use hand sanitizer and/or wash my hands '
                     'after shaking someone\'s hand',
        max_length=20,
        choices=AGREE_DISAGREE)

    avoid_public_places = models.CharField(
        verbose_name='I avoid going to public places',
        max_length=20,
        choices=AGREE_DISAGREE)

    class Meta(CrfModelMixin.Meta):
        app_label = 'esr21_subject'
        verbose_name = 'COVID Preventative Behaviours'
        verbose_name_plural = 'COVID Preventative Behaviours'
