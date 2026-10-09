import unittest

from labels import format_item_count


class FormatItemCountTests(unittest.TestCase):
    def test_singular(self):
        self.assertEqual(format_item_count(1), "1 item")

    def test_plural(self):
        self.assertEqual(format_item_count(3), "3 items")


if __name__ == "__main__":
    unittest.main()
