import unittest

from pymusicterm.util.time import milliseconds_to_minutes, milliseconds_to_seconds, seconds_to_milliseconds

class TestTime(unittest.TestCase):

    def setUp(self) -> None:
        #Example of song that last 3:45
        self.total_seconds:float=224.679125
        self.milliseconds:int=224680
        self.minutes:int=3
        self.seconds:int=45

    def test_milliseconds_to_minutes(self):
        self.assertEqual(milliseconds_to_minutes(self.milliseconds),self.minutes)

    def test_milliseconds_to_seconds(self):
        self.assertTrue(44 <= milliseconds_to_seconds(self.milliseconds) <= 46)

    def test_seconds_to_milliseconds(self):
        self.assertEqual(seconds_to_milliseconds(self.total_seconds),224680)

    def tearDown(self) -> None:
        del(self.total_seconds)
        del(self.milliseconds)
        del(self.minutes)
        del(self.seconds)

if __name__ == "__main__":
    unittest.main()
