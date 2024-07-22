import unittest

from models.ctal import CTAL


class MyTestCase(unittest.TestCase):
    ctal = CTAL()
    def test_ctal_data_init(self):
        self.ctal.printdata()
        self.assertEqual(True, True)  # add assertion here


if __name__ == '__main__':
    unittest.main()
