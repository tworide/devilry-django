from datetime import datetime, timedelta
from django.test import TestCase

from devilry.apps.core.testhelper import TestHelper
from devilry.utils.rest_testclient import RestClient
from devilry.apps.core.models import Deadline
from devilry.utils.restformat import format_datetime

from devilry_subjectadmin.rest.deadlinesbulk import encode_bulkdeadline_id
from devilry_subjectadmin.rest.deadlinesbulk import decode_bulkdeadline_id
from devilry_subjectadmin.rest.deadlinesbulk import sha1hash


class TestDeadlinesBulkRest(TestCase):
    def setUp(self):
        self.testhelper = TestHelper()
        self.testhelper.add(nodes='uni',
                            subjects=['sub'],
                            periods=['p1:begins(-2)'], # 2 months ago
                            assignments=['a1:admin(adm):pub(0)']) # 0 days after period begins
        self.client = RestClient()
        self.url = '/devilry_subjectadmin/rest/deadlinesbulk/{0}/'.format(self.testhelper.sub_p1_a1.id)

    def _listas(self, username, **data):
        self.client.login(username=username, password='test')
        return self.client.rest_get(self.url, **data)

    def test_get_empty(self):
        content, response = self._listas('adm')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(content), 0)

    def test_get_simple(self):
        for groupnum in xrange(3):
            # deadline 5 days after assignment starts
            self.testhelper.add_to_path('uni;sub.p1.a1.g{0}.d1:ends(5)'.format(groupnum))
        content, response = self._listas('adm')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(content), 1)
        d1 = content[0]
        self.assertEquals(set(d1.keys()),
                          set(['deadline', 'text', 'groupcount', 'offset_from_now',
                               'in_the_future', 'bulkdeadline_id']))
        self.assertEquals(d1['groupcount'], 3)
        self.assertEquals(d1['in_the_future'], False)
        self.assertEquals(d1['text'], None)

    def test_get_textdifference(self):
        for groupnum in xrange(3):
            # deadline 5 days after assignment starts
            self.testhelper.add_to_path('uni;sub.p1.a1.g{0}.d1:ends(5)'.format(groupnum))
        # Change text on g1_d1, which should make it a separate entry in the list
        self.testhelper.sub_p1_a1_g1_d1.text = 'Test'
        self.testhelper.sub_p1_a1_g1_d1.save()
        content, response = self._listas('adm')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(content), 2)
        g2_g3_d1 = content[0]
        g1_d1 = content[1]
        self.assertEquals(g1_d1['text'], 'Test')
        self.assertEquals(g1_d1['groupcount'], 1)
        self.assertEquals(g2_g3_d1['text'], None)
        self.assertEquals(g2_g3_d1['groupcount'], 2)

    def test_get_multiple_and_order(self):
        for groupnum in xrange(3):
            # deadline 5 days after assignment starts
            self.testhelper.add_to_path('uni;sub.p1.a1.g{0}.d1:ends(5)'.format(groupnum))
        for groupnum in xrange(2):
            # deadline 70 days after assignment starts, which should be in the future
            self.testhelper.add_to_path('uni;sub.p1.a1.g{0}.d2:ends(70)'.format(groupnum))
        content, response = self._listas('adm')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(content), 2)
        d1 = content[1]
        d2 = content[0]
        self.assertEquals(d1['groupcount'], 3)
        self.assertEquals(d1['in_the_future'], False)
        self.assertEquals(d2['groupcount'], 2)
        self.assertEquals(d2['in_the_future'], True)

    def test_get_nobody(self):
        self.testhelper.create_user('nobody')
        content, response = self._listas('nobody')
        self.assertEquals(response.status_code, 403)


class TestUpdateDeadlinesBulkRest(TestCase):
    def setUp(self):
        self.testhelper = TestHelper()
        self.testhelper.add(nodes='uni',
                            subjects=['sub'],
                            periods=['p1:begins(-2)']) # 2 months ago 
        self.testhelper.sub_p1.start_time = datetime(2000, 1, 1, 22, 30, 49)
        self.testhelper.sub_p1.save()
        self.testhelper.add_to_path('uni;sub.p1.a1:admin(adm):pub(0)') # 0 days after period begins + 2 sec
        self.client = RestClient()

        for groupnum in xrange(3):
            # deadline 5 days after assignment starts
            self.testhelper.add_to_path('uni;sub.p1.a1.g{0}.d1:ends(5)'.format(groupnum))


    def _geturl(self):
        bulkdeadline_id = encode_bulkdeadline_id(self.testhelper.sub_p1_a1_g1_d1)
        return '/devilry_subjectadmin/rest/deadlinesbulk/{0}/{1}'.format(self.testhelper.sub_p1_a1.id,
                                                                         bulkdeadline_id)

    def test_encode_unique_bulkdeadline_id(self):
        d = Deadline(deadline=datetime(2000, 12, 24, 22, 30, 49))
        self.assertEquals(encode_bulkdeadline_id(d),
                          '2000-12-24T22_30_49--')
        d.text = 'Hello world'
        self.assertEquals(encode_bulkdeadline_id(d),
                          '2000-12-24T22_30_49--{0}'.format(sha1hash('Hello world')))
        # Ensure unicode works
        d.text = u'\u00e5ello world'
        self.assertEquals(encode_bulkdeadline_id(d),
                          '2000-12-24T22_30_49--{0}'.format(sha1hash(u'\u00e5ello world')))


    def test_decode_unique_bulkdeadline_id(self):
        self.assertEquals(decode_bulkdeadline_id('2000-12-24T22_30_49--'),
                          (datetime(2000, 12, 24, 22, 30, 49), ''))
        self.assertEquals(decode_bulkdeadline_id('2000-12-24T22_30_49--{0}'.format(sha1hash('Hello world'))),
                          (datetime(2000, 12, 24, 22, 30, 49), sha1hash('Hello world')))


    def _putas(self, username, data):
        self.client.login(username=username, password='test')
        return self.client.rest_put(self._geturl(), data)

    def test_put(self):
        self.assertEquals(self.testhelper.sub_p1_a1.publishing_time, datetime(2000, 1, 1, 22, 30, 51))
        self.assertEquals(self.testhelper.sub_p1_a1_g1_d1.deadline,
                          datetime(2000, 1, 1, 22, 30, 51) + timedelta(days=5))

        new_deadline = datetime(2004, 12, 24, 20, 30, 40)
        content, response = self._putas('adm', {'deadline': format_datetime(new_deadline),
                                                'text': 'Hello'})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(decode_bulkdeadline_id(content['bulkdeadline_id'])[0],
                          new_deadline)
        self.assertEquals(len(content['groups']), 3)
        for groupnum in xrange(3):
            deadline_id = getattr(self.testhelper, 'sub_p1_a1_g{0}_d1'.format(groupnum)).id
            deadline = Deadline.objects.get(id=deadline_id)
            self.assertEquals(deadline.deadline, new_deadline)
            self.assertEquals(deadline.text, 'Hello')

    def test_put_nonetext(self):
        self.assertEquals(self.testhelper.sub_p1_a1.publishing_time, datetime(2000, 1, 1, 22, 30, 51))
        self.assertEquals(self.testhelper.sub_p1_a1_g1_d1.deadline,
                          datetime(2000, 1, 1, 22, 30, 51) + timedelta(days=5))

        new_deadline = datetime(2004, 12, 24, 20, 30, 40)
        content, response = self._putas('adm', {'deadline': format_datetime(new_deadline),
                                                'text': None})
        self.assertEquals(response.status_code, 200)
        for groupnum in xrange(3):
            deadline_id = getattr(self.testhelper, 'sub_p1_a1_g{0}_d1'.format(groupnum)).id
            deadline = Deadline.objects.get(id=deadline_id)
            self.assertEquals(deadline.deadline, new_deadline)
            self.assertEquals(deadline.text, '')

    def test_put_before_publishingtime(self):
        new_deadline = datetime(1990, 1, 1, 20, 30, 40)
        content, response = self._putas('adm', {'deadline': format_datetime(new_deadline),
                                                'text': None})
        self.assertEquals(response.status_code, 400)
        self.assertEquals(content['errors'], ['Deadline cannot be before publishing time.'])

    def test_put_nobody(self):
        self.testhelper.create_user('nobody')
        content, response = self._putas('nobody', {})
        self.assertEquals(response.status_code, 403)


    def _getas(self, username, **data):
        self.client.login(username=username, password='test')
        return self.client.rest_get(self._geturl(), **data)

    def test_get(self):
        content, response = self._getas('adm')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(decode_bulkdeadline_id(content['bulkdeadline_id'])[0],
                          self.testhelper.sub_p1_a1_g1_d1.deadline)
        self.assertEquals(content['deadline'],
                          format_datetime(self.testhelper.sub_p1_a1_g1_d1.deadline))
        self.assertEquals(content['text'], None)
        self.assertEquals(len(content['groups']), 3)

    def test_get_nobody(self):
        self.testhelper.create_user('nobody')
        content, response = self._getas('nobody')
        self.assertEquals(response.status_code, 403)
