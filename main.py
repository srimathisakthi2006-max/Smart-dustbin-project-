from machine import Pin, PWM
import time

# HC-SR04
TRIG = Pin(5, Pin.OUT)
ECHO = Pin(18, Pin.IN)

# Servo
SERVO = PWM(Pin(13), freq=50)

# LEDs
GREEN_LED = Pin(26, Pin.OUT)
RED_LED = Pin(27, Pin.OUT)


# -------------------------
# Servo
# -------------------------

def servo_angle(angle):

    min_duty = 26
    max_duty = 128

    duty = int(
        min_duty + (angle / 180) * (max_duty - min_duty)
    )

    SERVO.duty(duty)


# -------------------------
# Distance
# -------------------------

def get_distance():

    TRIG.value(0)
    time.sleep_us(2)

    TRIG.value(1)
    time.sleep_us(10)

    TRIG.value(0)

    start = time.ticks_us()

    while ECHO.value() == 0:

        if time.ticks_diff(time.ticks_us(), start) > 30000:
            return -1

    start = time.ticks_us()

    while ECHO.value() == 1:

        if time.ticks_diff(time.ticks_us(), start) > 30000:
            return -1

    duration = time.ticks_diff(
        time.ticks_us(),
        start
    )

    distance = (duration * 0.0343) / 2

    return distance


# -------------------------
# Initial state
# -------------------------

servo_angle(0)

GREEN_LED.value(0)
RED_LED.value(1)


# -------------------------
# Main loop
# -------------------------

while True:

    distance = get_distance()

    print("Distance:", distance, "cm")

    # Object detected
    if distance > 0 and distance <= 20:

        print("Object detected!")
        print("Opening dustbin...")

        # Green ON
        GREEN_LED.value(1)
        RED_LED.value(0)

        # Open lid
        servo_angle(90)

        # Keep open
        time.sleep(3)

        # Close lid
        print("Closing dustbin...")
        servo_angle(0)

        GREEN_LED.value(0)
        RED_LED.value(1)

        # IMPORTANT:
        # Wait until object moves away
        print("Waiting for object to move away...")

        while True:

            distance = get_distance()

            print("Waiting:", distance, "cm")

            if distance > 20:

                break

            time.sleep(0.5)

        print("Ready for next object!")

    time.sleep(0.5)
