#!/usr/bin/env python

import unittest

from pydarts.communication import (get_input, sanitized_input,
        SanitizationError, MinLargerMaxError)


class SanitizedInputTestCase(unittest.TestCase):

    def test_min_larger_max(self):
        self.assertRaises(MinLargerMaxError, sanitized_input, "foo",
                method="testing", min_=1, max_=0)

    def test_wrong_type(self):
        self.assertRaises(SanitizationError, sanitized_input, "foo",
                method="testing", type_=int)

    def test_too_large(self):
        self.assertRaises(SanitizationError, sanitized_input, "42",
                method="testing", type_=int, max_=11)

    def test_too_small(self):
        self.assertRaises(SanitizationError, sanitized_input, "42",
                method="testing", type_=int, min_=1337)

    def test_too_short(self):
        self.assertRaises(SanitizationError, sanitized_input, "bar",
                method="testing", min_=5)

    def test_valid_str(self):
        self.assertEqual(sanitized_input("süß", method="testing", min_=1), "süß")

    def test_valid_int(self):
        self.assertEqual(sanitized_input("123", method="testing", type_=int, max_=180), 123)


class TestInputTestCase(unittest.TestCase):

    def test_min_larger_max(self):
        self.assertRaises(MinLargerMaxError, get_input, "25", method="testing",
                min_=10, max_=9)

    def test_valid_str(self):
        self.assertEqual(get_input("Phil11!", method="testing"), "Phil11!")


if __name__ == "__main__":
    unittest.main()
