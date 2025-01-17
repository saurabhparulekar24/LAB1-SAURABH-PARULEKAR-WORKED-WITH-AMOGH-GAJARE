import board
import busio
import neopixel
import adafruit_apds9960.apds9960
from time import sleep
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

#initialization of Sensor Board APDS9960
i2c = board.STEMMA_I2C()#Initializing the I2C port for Qwwic Connector
sensor = adafruit_apds9960.apds9960.APDS9960(i2c)

#mode Enable
sensor.color_integration_time = 255 #ADC Intergration time/Number of Cycles/Count   color_integration_time:time(255:2.78ms,219:103ms)
sensor.enable_color = True #Enable Color Sensor

#CircuitPy HID Keyboard Initialization
sleep(1)  # Sleep for a bit to avoid a race condition on some systems
keyboard = Keyboard(usb_hid.devices) #Connect as a keyboard
keyboard_layout = KeyboardLayoutUS(keyboard)

bar_previous = 0 #Historical variable for the brightness
while True:
    r, g, b, c = sensor.color_data
    if c >= 50: #To avoid the keyboard to go Crazy, before starting the code the sensor needs to be covered
        r, g, b, c = sensor.color_data
        bar = int(c*50/65535) #Converting to a scale of 50
        if bar-bar_previous > 0: #If brightness increases, type 'O'
            for i in range(abs(bar-bar_previous)):
                keyboard.press(Keycode.SHIFT,Keycode.O)
                keyboard.release_all()
        elif bar - bar_previous < 0: # If brightness Decreases, type BACKSPACE
            for i in range(abs(bar-bar_previous)):
                keyboard.press(Keycode.BACKSPACE)
                keyboard.release_all()
        bar_previous = bar



