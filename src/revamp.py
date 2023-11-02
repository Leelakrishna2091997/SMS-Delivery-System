# Import necessary libraries
import queue
import random
import string
import threading
import time

# Define a Producer class responsible for generating messages and phone numbers
class Producer:
    # Initialize the Producer with a queue and a default message count
    def __init__(self, messageQueue, messagesCount=1000):
        # Call to the superclass initializer is not necessary since it's not extending another class
        try:
            if(messagesCount <= 0):
                raise Exception  # Raise an exception if the message count is not positive
            self.messagesCount = messagesCount
            self.queue = messageQueue
            # Populate the queue with random messages and phone numbers
            for _ in range(self.messagesCount):
                phone_number = ''.join(random.choices(string.digits, k=10))
                message = ''.join(random.choices(string.ascii_letters + string.digits + ' ', k=random.randint(10, 100)))
                self.queue.put((phone_number, message))
        except Exception as e:
            raise ValueError("Error in message production")  # Raise a ValueError if an exception occurs

    # Method to generate normally distributed values
    def generate_normal_values(self, mean, n):
        # Define standard deviation as a fraction of the mean
        deviation = mean * 0.1
        # Generate n random values from the normal distribution
        values = [random.gauss(mean, deviation) for eachNumber in range(n)]
        # Calculate the mean of the generated values
        valueMean = sum(values) / n
        # Adjust the values to match the specified mean and round them to two decimal places
        distributionValues = [round(eachValue - valueMean + mean, 2) for eachValue in values]
        return distributionValues

    # Method to generate a random 10-digit phone number
    def random_phone_number(self):
        return ''.join(random.choice(string.digits) for _ in range(10))

    # Method to generate a random message with characters up to 100
    def random_message(self):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(random.randint(1, 100)))

    # Method to produce messages and add them to the queue
    def produce(self):
        for _ in range(self.num_messages):
            phone_number = self.random_phone_number()
            message = self.random_message()
            self.queue.put((phone_number, message))  # Add the (phone_number, message) tuple to the queue


# Define a Sender class that extends the Thread class
class Sender(threading.Thread):
    # Initialize the Sender with a queue, processing time, failure rate, and an ID
    def __init__(self, queue, proc_time, failure_rate, senderId):
        super(Sender, self).__init__()  # Call the superclass initializer
        self.queue = queue
        self.senderId = senderId
        self.proc_time = proc_time
        self.failure_rate = failure_rate
        self.sent_count = 0
        self.failed_count = 0
        self.total_time = 0

    # The run method is the entry point for a thread
    def run(self):
        while True:
            try:
                # Fetch a message from the queue with a timeout of 1 second
                phone_number, message = self.queue.get(timeout=1)
                time.sleep(self.proc_time)  # Simulate processing time
                predict = random.random()
                # Determine if the message sending is successful or failed
                if predict < self.failure_rate:
                    self.failed_count += 1
                else:
                    self.sent_count += 1
                self.total_time += self.proc_time
                self.queue.task_done()
            except queue.Empty:
                break  # If the queue is empty, break from the loop


# Define a ProgressMonitor class that extends the Thread class
class ProgressMonitor(threading.Thread):
    # Initialize the monitor with a list of senders and an update interval
    def __init__(self, senders, update_interval):
        super().__init__()  # Call the superclass initializer
        self.senders = senders
        self.update_interval = update_interval
        self.running = True

    # The run method is the entry point for a thread
    def run(self):
        while self.running:
            self.display()  # Display the progress
            time.sleep(self.update_interval)  # Wait for the update interval before refreshing

    # Method to display the current progress of message sending
    def display(self):
        total_sent = sum(eachSender.sent_count for eachSender in self.senders)
        total_failed = sum(eachSender.failed_count for eachSender in self.senders)
        total_processed = total_sent + total_failed
        # Calculate the average time per message
        avg_time = (sum(eachSender.total_time for eachSender in self.senders) / total_processed) if total_processed else 0
        # Print the current progress
        print("Monitor:")
        print(f"Number of messages sent: {total_sent}")
        print(f"Number of messages failed: {total_failed}")
        print(f"Average time per message: {avg_time:.2f} seconds\n")

    # Method to stop the monitoring
    def stop(self):
        self.running = False


# The main block that runs when the script is executed directly
if __name__ == '__main__':
    numMessages = int(input("Enter the number of messages to produce: "))
    numSenders = int(input("Enter the number of senders: "))
    meanTime = float(input("Enter the mean processing time for senders: "))
    failureRateMean = float(input("Enter the mean failure rate for senders: 0 to 1: "))
    update_interval = int(input("Enter the monitor refresh time in seconds: "))

    # Create a message queue and a producer
    message_queue = queue.Queue()
    producer = Producer(message_queue, numMessages)
    # Generate distributions for processing times and failure rates
    procTimes = producer.generate_normal_values(meanTime, numSenders)
    failureRates = producer.generate_normal_values(failureRateMean, numSenders)
    senders = []
    # Print the generated distributions
    print("Processing times distribution: " + str(procTimes))
    print("Failure rates distribution: " + str(failureRates))
    # Create sender threads
    for i in range(numSenders):
        senders.append(Sender(message_queue, procTimes[i], failureRates[i], i))
    # Create and start the progress monitor thread
    monitor = ProgressMonitor(senders, update_interval)
    for sender in senders:
        sender.start()
    monitor.start()
    # Wait for all senders to finish
    for sender in senders:
        sender.join()
    # Display the final results and stop the monitor
    monitor.display()
    monitor.stop()
