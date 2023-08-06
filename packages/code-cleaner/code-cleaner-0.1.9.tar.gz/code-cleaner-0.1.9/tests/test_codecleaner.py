#!/usr/bin/env python

"""Tests for `codecleaner` package."""
import os
import unittest

from codecleaner.cleaner import CopyrightCleaner, CommentsCleaner


class TestStringMethods(unittest.TestCase):
    def test_clean_documentation(self):
        cleaner = CopyrightCleaner("")

        with open("tests/samples/documentation_1_original.txt", "rt", encoding="utf8") as orig, \
                open("tests/samples/documentation_1_clean.txt", "rt", encoding="utf8") as cln:
            original = orig.read()

            cleaned = cleaner.run(original).strip().replace(" ", "")

            clean = cln.read().strip().replace(" ", "")

            self.assertEqual(clean, cleaned)

    def test_clean_comments(self):
        self.maxDiff = None

        cleaner = CommentsCleaner("")
        print(os.getcwd())
        with open("tests/samples/comments_1_original.txt", "rt", encoding="utf8") as orig, \
                open("tests/samples/comments_1_clean.txt", "rt", encoding="utf8") as cln:
            original = orig.read()

            cleaned = cleaner.run(original).strip().replace(" ", "")

            clean = cln.read().strip().replace(" ", "")

            self.assertEqual(clean, cleaned)


if __name__ == '__main__':
    unittest.main()
