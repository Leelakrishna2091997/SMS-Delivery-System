import queue
import unittest
from unittest.mock import patch

from revamp import Producer


class TestProducer(unittest.TestCase):

    """ Testing 2000 messages produced with each message having length less than or equal to 100 and have a phone number with 10 digits."""

    def test_message_production(self):
        self.numMessages = 2000
        self.queue = queue.Queue()
        self.producer = Producer(self.queue, self.numMessages)
        self.assertEqual(self.queue.qsize(), self.numMessages)
        while not self.queue.empty():
            phone_number, message = self.queue.get()
            self.assertEqual(len(phone_number), 10)
            self.assertLessEqual(len(message), 100)

    """ Negative messages cannot be produced."""
    def test_message_production_negative(self):
        with self.assertRaises(ValueError) as context:
            self.numMessages = -1
            self.queue = queue.Queue()
            self.producer = Producer(self.queue, self.numMessages)

        # Testing for exact message.
        self.assertEqual(str(context.exception), "Error in message production")


if __name__ == '__main__':
    unittest.main()
