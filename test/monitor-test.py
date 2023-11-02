import queue
import time
import unittest
from unittest.mock import patch, MagicMock

from revamp import Sender, ProgressMonitor


class TestProgressMonitor(unittest.TestCase):

    """
    No messages are being produced, only testing the functionality of the monitor.
    """

    def setUp(self):
        q = queue.Queue()
        self.senders = [Sender(q, 1, 0, _) for _ in range(2)]
        self.updateInterval = 3  # Set the refresh interval to 3 seconds for the test
        self.monitor = ProgressMonitor(self.senders, self.updateInterval)


    def test_monitor_stopping(self):
        self.monitor.start()
        self.monitor.stop()
        self.monitor.join()
        self.assertFalse(self.monitor.running)


    @patch('revamp.time.sleep', side_effect=lambda x: None)
    def test_monitor_display_called_once(self, mock_sleep):
        """ Test that the display method is called exactly once during the given time period. """
        with patch.object(self.monitor, 'display', wraps=self.monitor.display) as mock_display:
            self.monitor.start()
            time.sleep(3)
            self.monitor.stop()
            self.monitor.join()

        # Display is called once.
        mock_display.assert_called_once()

        # Identify sleep is called with the update interval.
        mock_sleep.assert_called_with(self.updateInterval)

    @patch('revamp.time.sleep', side_effect=lambda x: None)
    def test_monitor_update_interval(self, mock_sleep):
        """ Test that the monitor waits for the update interval before calling display. """
        with patch.object(self.monitor, 'display', wraps=self.monitor.display) as mock_display:
            self.monitor.start()
            time.sleep(3)
            self.monitor.stop()
            self.monitor.join()

        # Display is called.
        self.assertTrue(mock_display.called)

        # Identify sleep is called with update interval.
        mock_sleep.assert_called_with(self.updateInterval)


if __name__ == '__main__':
    unittest.main()
