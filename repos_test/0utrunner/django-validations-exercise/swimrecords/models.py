from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as text
from django.core.validators import *
from datetime import timedelta
from django.utils import timezone


def validate_stroke(stroke):
    stroke_types = ['front crawl', 'butterfly', 'breast', 'back', 'freestyle']
    if stroke not in stroke_types:
        raise ValidationError(text(
            f'{stroke} is not a valid stroke'))


def valid_relay(relay):
    valid = ['True', 'False']
    if relay not in valid:
        raise ValidationError(text(
            f"'None' value must be either True or False."))


def bad_future(record_date):
    if record_date > timezone.now():
        raise ValidationError(text(
            f"Can't set record in the future."))


def no_future(record_broken_date):
    if record_broken_date < timezone.now() - timedelta(days=1):
        raise ValidationError(text(
            f"Can't break record before record was set."))


class SwimRecord(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    team_name = models.CharField(max_length=255)
    relay = models.BooleanField(default=False, validators=[valid_relay])
    stroke = models.CharField(max_length=255, validators=[validate_stroke])
    distance = models.IntegerField(validators=[MinValueValidator(50)])
    record_date = models.DateTimeField(validators=[bad_future])
    record_broken_date = models.DateTimeField(validators=[no_future])
