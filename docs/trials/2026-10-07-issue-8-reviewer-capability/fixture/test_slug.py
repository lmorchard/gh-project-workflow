import unittest
from slug import slug

class SlugTests(unittest.TestCase):
    def test_words(self):
        self.assertEqual(slug("Hello World"), "hello-world")

if __name__ == "__main__":
    unittest.main()
