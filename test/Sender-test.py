import queue
import unittest
from unittest.mock import patch

from revamp import Sender


class TestSender(unittest.TestCase):
    def setUp(self):
        self.queue = queue.Queue()
        self.mean_time = 0.01
        self.failure_rate = 0
        self.sender = Sender(self.queue, self.mean_time, self.failure_rate, 1)

    @patch('revamp.random.gauss')
    @patch('revamp.random.random')
    def test_message_sending(self, mock_random, mock_gauss):
        mock_gauss.return_value = self.mean_time
        mock_random.return_value = 0 
        for _ in range(10):
            self.queue.put(('1234567890', 'Test Message'))
        while not self.queue.empty():
            self.sender.run()
        self.assertEqual(self.sender.sent_count, 10)
        self.assertEqual(self.sender.failed_count, 0)
