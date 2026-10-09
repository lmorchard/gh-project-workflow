import unittest

from labels import format_item_count


class ItemCountTests(unittest.TestCase):
    def test_one_uses_singular(self):
        self.assertEqual(format_item_count(1), "1 item")

    def test_other_counts_use_plural(self):
        for count in (0, 2, 7, 1000000):
            with self.subTest(count=count):
                self.assertEqual(format_item_count(count), f"{count} items")
