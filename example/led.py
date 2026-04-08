from machine import Pin

gpio=Pin(Pin.GPIO29,Pin.OUT,Pin.PULL_DISABLE,0)
gpio.write(1)
print("LED is on")
