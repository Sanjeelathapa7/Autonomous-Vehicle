import serial
import time
import keyboard

# Replace 'COM3' with your Arduino's serial port
ser = serial.Serial('COM4', 9600, timeout=1)

def set_speed(speed):
    # Send speed value to Arduino
    ser.write(str(speed).encode())

if __name__ == "__main__":
    try:
        speed = 1500  # Initial speed
        while True:
            if keyboard.is_pressed('w'):
                speed += 200
                speed = min(speed, 2000)  # Limit speed to maximum 2000
                set_speed(speed)
                print("Speed increased to:", speed)
                time.sleep(0.1)
            elif keyboard.is_pressed('s'):
                speed -= 200
                speed = max(speed, 1000)  # Limit speed to minimum 1000
                set_speed(speed)
                print("Speed decreased to:", speed)
                time.sleep(0.1)
            elif keyboard.is_pressed('q'):
                break  # Exit loop if 'q' is pressed
    except KeyboardInterrupt:
        ser.close()
