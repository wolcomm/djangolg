from __future__ import print_function
from __future__ import unicode_literals

from django.test import TestCase


class FooTestCase(TestCase):
    def test_foo(self):
        self.assertEqual(1+1, 2)
