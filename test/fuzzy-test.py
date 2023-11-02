import queue
import time
import unittest
from unittest.mock import patch
from revamp import Producer, Sender

class TestProducerAndSender(unittest.TestCase):

    def initializeData(self, noOfMessages, noOfSenders, meanProc, meanFail):
        self.numMessages = noOfMessages
        self.numSenders = noOfSenders
        self.meanTime = meanProc
        self.failureRateMean = meanFail
        self.queue = queue.Queue()
        self.producer = Producer(self.queue, self.numMessages)
        procTimes = self.producer.generate_normal_values(self.meanTime, self.numSenders)
        failureRates = self.producer.generate_normal_values(self.failureRateMean, self.numSenders)
        print("Processing times distribution: " + str(procTimes))
        print("Failure rates distribution: " + str(failureRates))
        self.senders = []
        for i in range(self.numSenders):
            self.senders.append(Sender(self.queue, procTimes[i], failureRates[i], i))

    def test_message_production(self):
        self.initializeData(10, 1, 1, 0)
        """Test that the producer generates the correct number of messages."""
        self.assertEqual(self.queue.qsize(), self.numMessages)

    def setUp(self):
        self.initializeData(2000, 3, 1, 0.1)


    @patch('revamp.random.gauss')
    @patch('revamp.random.random')
    @patch('revamp.time.sleep')
    def test_sender_processing(self, mock_sleep, mock_random_fail, mock_random_time):

        """Test that senders process messages without exceeding mean processing time."""
        mock_random_fail.return_value = 1

        # Start and run the senders to process the queue
        for sender in self.senders:
            sender.run()

        # Calculating average processing time and failure rate
        total_time_taken = sum(sender.total_time for sender in self.senders)
        total_messages_processed = sum(sender.sent_count for sender in self.senders)
        average_time = total_time_taken / total_messages_processed

        # Check that the average time does not exceed the mean time
        self.assertAlmostEqual(average_time, self.meanTime, delta=0.5)

if __name__ == '__main__':
    unittest.main()
