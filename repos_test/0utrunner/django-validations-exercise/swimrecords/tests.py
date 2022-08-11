from django.test import TestCase
from .models import SwimRecord
from django.core.exceptions import ValidationError
from datetime import timedelta
from django.utils import timezone


class SwimRecordTestCase(TestCase):

    record = SwimRecord()

    def test_01_validate_first_name_presence(self):
        """validates presence of first_name"""
        try:
            self.record.full_clean()
            raise Exception("full_clean should throw a validation error")
        except ValidationError as e:
            self.assertTrue(
                'This field cannot be blank.' in e.message_dict['first_name'])

    def test_02_validate_last_name_presence(self):
        """validates presence of last_name"""
        try:
            self.record.full_clean()
            raise Exception("full_clean should throw a validation error")
        except ValidationError as e:
            self.assertTrue(
                'This field cannot be blank.' in e.message_dict['last_name'])

    def test_03_validate_team_name_presence(self):
        """validates presence of team_name"""
        try:
            self.record.full_clean()
            raise Exception("full_clean should throw a validation error")
        except ValidationError as e:
            self.assertTrue(
                'This field cannot be blank.' in e.message_dict['team_name'])

    def test_04_validate_relay_presence(self):
        """validates presence of relay"""
        try:
            self.record.full_clean()
            raise Exception("full_clean should throw a validation error")
        except ValidationError as e:
            self.assertTrue(
                "'None' value must be either True or False." in e.message_dict['relay'])

    def test_05_valid_stroke(self):
        """validates that the stroke is one of 'front crawl', 'butterfly', 'breast', 'back', or 'freestyle'"""
        stroke_record = SwimRecord(stroke='doggie paddle')
        try:
            stroke_record.full_clean()
            raise Exception("full_clean should throw a validation error")
        except ValidationError as e:
            self.assertTrue(
                "doggie paddle is not a valid stroke" in e.message_dict['stroke'])

    def test_06_valid_distance(self):
        """must be greater than or equal to 50"""
        distance_record = SwimRecord(distance=20)
        try:
            distance_record.full_clean()
            raise Exception("full_clean should throw a validation error")
        except ValidationError as e:
            self.assertTrue(
                "Ensure this value is greater than or equal to 50." in e.message_dict['distance'])

    def test_07_no_future_records(self):
        """does not allow records to be set in the future"""
        bad_date = timezone.now() + timedelta(days=1)
        record = SwimRecord(record_date=bad_date)
        try:
            record.full_clean()
            raise Exception("full_clean should throw a validation error")
        except ValidationError as e:
            self.assertTrue(
                "Can't set record in the future." in e.message_dict['record_date'])

    def test_08_no_break_record_before_set_record(self):
        """does not allow records to be broken before the record_date"""
        record = SwimRecord(first_name='j', last_name='j', team_name='k', relay=True, stroke='butterfly',
                            distance=100, record_date=timezone.now(), record_broken_date=(timezone.now() - timedelta(days=1)))
        record.save()
        try:
            record.full_clean()
            raise Exception("full_clean should throw a validation error")
        except ValidationError as e:
            self.assertTrue(
                "Can't break record before record was set." in e.message_dict['record_broken_date'])
