from django.test import TestCase

from devilry.apps.core.testhelper import TestHelper
from devilry.apps.subjectadmin.rest.auth import (subjectadmin_required,
                                                 periodadmin_required,
                                                 assignmentadmin_required)
from devilry.apps.subjectadmin.rest.errors import PermissionDeniedError


class TestSubjectadminRequired(TestCase):
    def setUp(self):
        self.testhelper = TestHelper()
        self.testhelper.add(nodes='uni',
                            subjects=['s1:admin(s1admin)', 's2'])
        self.testhelper.create_superuser("superuser")

    def test_superuser(self):
        subjectadmin_required(self.testhelper.superuser, "", None) # Calls is_superuser and exits without further checks

    def test_admin_allowed(self):
        subjectadmin_required(self.testhelper.s1admin, "",
                                 self.testhelper.s1.id)

    def test_nonadmin_denied(self):
        self.assertRaises(PermissionDeniedError,
                          subjectadmin_required, self.testhelper.s1admin,
                          "", self.testhelper.s2.id) # s1admin is not admin on s2..

class TestPeriodadminRequired(TestCase):
    def setUp(self):
        self.testhelper = TestHelper()
        self.testhelper.add(nodes='uni',
                            subjects=['sub'],
                            periods=['p1:admin(p1admin)', 'p2'])
        self.testhelper.create_superuser("superuser")

    def test_superuser(self):
        periodadmin_required(self.testhelper.superuser, "", None) # Calls is_superuser and exits without further checks

    def test_admin_allowed(self):
        periodadmin_required(self.testhelper.p1admin, "",
                                 self.testhelper.sub_p1.id)

    def test_nonadmin_denied(self):
        self.assertRaises(PermissionDeniedError,
                          periodadmin_required, self.testhelper.p1admin,
                          "", self.testhelper.sub_p2.id) # p1admin is not admin on p2..


class TestAssignmentAdminRequired(TestCase):
    def setUp(self):
        self.testhelper = TestHelper()
        self.testhelper.add(nodes='uni',
                            subjects=['duck1010'],
                            periods=['firstsem'],
                            assignments=['a1:admin(a1admin)', 'a2'])
        self.testhelper.create_superuser("superuser")
        self.assignment1 = self.testhelper.duck1010_firstsem_a1
        self.assignment2 = self.testhelper.duck1010_firstsem_a2

    def test_superuser(self):
        assignmentadmin_required(self.testhelper.superuser, "", None) # Calls is_superuser and exits without further checks

    def test_admin_allowed(self):
        assignmentadmin_required(self.testhelper.a1admin, "",
                                 self.assignment1.id)

    def test_nonadmin_denied(self):
        self.assertRaises(PermissionDeniedError,
                          assignmentadmin_required, self.testhelper.a1admin,
                          "", self.assignment2.id) # a1admin is not admin on a2
