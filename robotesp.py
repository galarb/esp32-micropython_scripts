import machine
import time
from lcd_api import LcdApi
from i2c_lcd import I2cLcd
from pidcalc_module import pidcalc
from ggg import HCSR04
from machine import Pin, PWM, SoftI2C
from time import sleep

I2C_ADDR = 0x27
totalRows = 2
totalColumns = 16

#NOTE: for PWM pins: 34-39 cannot be used
echo_pin = 32	
trigger_pin = 17
servopin = machine.Pin(16)
servo_pwm = machine.PWM(servopin)
servo_pwm.freq(50)  # Adjust the frequency if needed
radarspeed = 1
radarangle = 0

sensor = HCSR04(trigger_pin, echo_pin, echo_timeout_us=10000)
i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=10000) #I2C for ESP32
lcd = I2cLcd(i2c, I2C_ADDR, totalRows, totalColumns)





#servo go to angle. converts angle to DC
def set_servo_position(angle):
    duty_cycle = int((angle / 180) * 1023)  # Map angle to duty cycle
    servo_pwm.duty(duty_cycle)


#scanning procedure
def scan():
    print("scanning")
    for i in range(0, 180):
        set_servo_position(i) 
        sleep(0.2)
        radarangle = i
        print(i)
    for i in range(180, 0):
        set_servo_position(i) 
        sleep(0.4)
        radarangle = i
        print(i)    
"""
#distance measuring procedure
def getdistance1():
    print("measuring distance3")
    trigger_pin.on()
    time.sleep_us(10)
    trigger_pin.off()
    while echo_pin.value() == 0:
        pulse_start = time.ticks_us()
    while echo_pin.value() == 1:
        pulse_end = time.ticks_us()
    pulse_duration = (pulse_end - pulse_start) 
    print(pulse_duration)
    speed_of_sound = 343  # meters per second
    distance = (pulse_duration * speed_of_sound) / 2
    print("Distance: %.2f cm" % (distance / 58))
    print("finished measuring")

"""

def getdistance():
    distance = sensor.distance_cm()
    return distance
    #print('Distance:', distance, 'cm')

#blink procedure
def blink(pinNo, deltime):
    print("blinking pin ", pinNo, " for " , deltime , "seconds")
    blinkingobj = machine.Pin(pinNo, machine.Pin.OUT) #Definition as output
    for i in range(0, deltime):
        blinkingobj.value(1)
        sleep(deltime)
        blinkingobj.value(0)
        sleep(deltime)



while True:
    print ('harro')
    sleep(1)
    #blink(3, 1)
    print(getdistance())
    #scan()
    lcd.putstr("XXXX")
    """
    set_servo_position(90)
    print("in 90 position")
    sleep(2)
    set_servo_position(180)
    print("in 180 position")
    sleep(2)
    """
    lcd.clear()
    pidcalc(90, 10, 1, 0, 0)
    sleep(2)








    
    