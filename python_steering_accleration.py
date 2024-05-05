import serial
import time
import keyboard

# Replace 'COM3' with your Arduino's serial port
ser = serial.Serial('COM4', 9600, timeout=1)

def send_command(command):
    ser.write(command.encode())

if __name__ == "__main__":
    try:
        while True:
            if keyboard.is_pressed('s'):
                send_command('F')
                print("Moving backward")
                time.sleep(0.1)
            elif keyboard.is_pressed('w'):
                send_command('B')
                print("Moving forward")
                time.sleep(0.1)
            elif keyboard.is_pressed('d'):
                send_command('L')
                print("Turning right")
                time.sleep(0.1)
            elif keyboard.is_pressed('a'):
                send_command('R')
                print("Turning left")
                time.sleep(0.1)
            elif keyboard.is_pressed('x'):
                send_command('S')
                print("Neutral")
                time.sleep(0.1)
            elif keyboard.is_pressed('q'):
                print("Stopping")
                break  # Exit loop if 'q' is pressed
    except KeyboardInterrupt:
        ser.close()
