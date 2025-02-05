import threading
import time
import msvcrt
# Define a function that will run in a separate thread
def wait_For_Input():
    while True:
        if msvcrt.kbhit():  # Check if a key is pressed
            key = msvcrt.getch()  # Get the key
            if key == b'a':  # Check if the pressed key is 'a'
                print("You pressed 'a'!")
            else:
                print(f"You pressed: {key.decode('utf-8')}")

# Define another function that will run in a separate thread
def print_letters():
    while True:
        for letter in 'ABCDE':
            time.sleep(0.5)  # Simulate some work
            print(f"Letter {letter}")

# Create two threads
thread1 = threading.Thread(target=wait_For_Input)
thread2 = threading.Thread(target=print_letters)

# Start the threads
thread1.start()
thread2.start()

# Wait for both threads to finish
thread1.join()
thread2.join()

print("Both threads have finished execution!")
