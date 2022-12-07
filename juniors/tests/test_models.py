from django.db.utils import IntegrityError
from rest_framework import status

from juniors.models import Junior, JunSchedule, User, Position
from slugify import slugify
from django.test import TestCase


class CalendarModelsTestCase(TestCase):
    def setUp(self):
        self.position = Position.objects.create(id=6, position='Client', slug='client')
        self.user1 = User.objects.create(username = 'Ivanov')
        self.user2 = User.objects.create(username='Petrov')
        self.junior1 = Junior.objects.create(username=self.user1, slug=slugify(self.user1.username))
        self.junior2 = Junior.objects.create(username=self.user2, slug=slugify(self.user2.username))
        self.app1 = JunSchedule.objects.create(junior_id=self.junior1, client_id=self.junior2, date='2022-10-29', time='13:00')
        self.response=self.client.get('django-ithunt.herokuapp.com')

    def test_single_appoinment_for_a_time(self):
        with self.assertRaises(IntegrityError):
            JunSchedule.objects.create(junior_id=self.junior1, client_id=self.junior2, date='2022-10-29', time='13:00')

    def test_next_hour_appointment(self):
        JunSchedule.objects.create(junior_id=self.junior1, client_id=self.junior2, date='2022-10-29', time='14:00')
        self.assertEqual(JunSchedule.objects.values('time').get(pk=2)['time'].strftime('%H:%M'), '14:00', 'Второе время не то')