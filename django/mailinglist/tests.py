from django.test import TestCase
from rest_framework.test import APITestCase
from unittest.mock import patch
from django.contrib.auth import get_user_model
from .models import Subscriber, MailingList
from .factories import SubscriberFactory
import json


# Create your tests here.
class MockSendEmailToSubscriberTask:

    def setUp(self):
        self.send_confirmation_email_path = patch('mailinglist.tasks.send_confirmation_email_to_subscriber')
        self.send_confirmation_email_mock = self.send_confirmation_email_path.start()
        super().setUp()

    def tearDown(self):
        self.send_confirmation_email_path.stop()
        self.send_confirmation_email_mock = None
        super().tearDown()


class SubscriberCreationTestCase(MockSendEmailToSubscriberTask, TestCase):

    def test_calling_create_queues_confirmation_email_task(self):
        user = get_user_model().objects.create_user(username='unit test')
        mailing_list = MailingList.objects.create(name='unit_test', owner=user)
        Subscriber.objects.create(email='email@mail.com', mailing_list=mailing_list)
        self.asserEqual(self.send_confirmation_email_mock.delay.call_count, 1)


class SubscriberManagerTestCase(TestCase):

    def testConfirmedSubscribersForMailingList(self):
        mailing_list = MailingList.objects.create(
            name='unit test',
            owner=get_user_model().objects.create_user(
                username='unit test')
        )
        confirmed_users = [
            SubscriberFactory(confirmed=True, mailing_list=mailing_list)
            for n in range(3)]
        unconfirmed_users = [
            SubscriberFactory(mailing_list=mailing_list)
            for n in range(3)]
        confirmed_users_qs = Subscriber.objects.confirmed_subscribers_for_mailing_list(
            mailing_list=mailing_list)
        self.assertEqual(len(confirmed_users), confirmed_users_qs.count())
        for user in confirmed_users_qs:
            self.assertIn(user, confirmed_users)


class ListMailingListWithAPITestCase(APITestCase):

    def setUp(self):
        username = 'test_user'
        password = 'test_password'
        self.user = get_user_model().objects.create_user(
                username = username,
                password = password
        )
        cred_bytes = f'{username}:{password}'.encode('utf-8')
        self.basic_auth = base64.b64encode(cred_bytes).decode('utf-8')

    def test_listing_all_my_mailinglist(self):
        mailing_lists = [MailingList.objects.create(
            name = f'list test {i}',
            owner = self.user)
            for i in range(3)
        ]

        self.client.credentials(HTTP_AUTHORIZATION=f'Basic {self.basic_auth}')

        response = self.client.get('api/v1/mailinglist')

        self.assertEqual(200, response.status_code)
        parsed = json.loads(response.content)
        self.assertEqual(3, len(parsed))

        content = str(response.content)
        for ml in mailinglists:
            self.assertIn(str(ml.id), content)

