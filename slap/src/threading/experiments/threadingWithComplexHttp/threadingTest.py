from webapp.serverMain import run as server_Main
import threading
import time
import msvcrt


# Define a function that will run in a separate thread
def webApp():
    server_Main()

# Define another function that will run in a separate thread
def detect_Input():
   while True:
        if msvcrt.kbhit():  # Check if a key is pressed
            key = msvcrt.getch()  # Get the key
            if key == b'a':  # Check if the pressed key is 'a'
                print("You pressed 'a'!")
            else:
                print(f"You pressed: {key.decode('utf-8')}")


# Create two threads
thread1 = threading.Thread(target=webApp)
thread2 = threading.Thread(target=detect_Input)

# Start the threads
thread1.start()
thread2.start()

# Wait for both threads to finish
thread1.join()
thread2.join()

print("Both threads have finished")
