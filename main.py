import random
import time
import utime
from machine import Pin, Timer
from neopixel import Neopixel
import micropython
timer = Timer()

buttonPIN = 19
button = Pin(buttonPIN, Pin.IN, Pin.PULL_DOWN)

numpix = 30
brightness = 150
pixels = Neopixel(numpix, 0, 28, "GRB")
pixels.brightness(brightness)

colorDict = dict()
colorDict['white'] = (255, 255, 255)
colorDict['red'] = (204, 0, 0)
colorDict['yellow'] = (225, 180, 0)
colorDict['green'] = (0, 102, 0)

lights = [range(0, 10), range(11, 20), range(20, 30)]
swirl_lights = [
    [9, 8, 7, 6, 5, 4, 3, 2, 1, 0],
    [19, 18, 17, 16, 15, 14, 13, 12, 11, 10],
    [29, 28, 27, 26, 25, 24, 23, 22, 21, 20 ],
    ]

show_counter = 0

def debounce(pin):
    timer.init(mode=Timer.ONE_SHOT, period=200, callback=button_callback)

def button_callback(pin):
    global show_counter
    show_counter += 1
    
def shimmer():
    global show_counter
    show_counter_orig = show_counter
    print('shimmer')
    for l in range(0, 10):
        pixels.clear()
        for x in range(0, 10):
            y = random.randint(0, numpix-1)
            pixels.set_pixel(y, colorDict['white'], random.randint(0, 150))
        pixels.show()
        time.sleep(0.2)
    if show_counter_orig != show_counter:
        return
    
def swirl():
    global show_counter
    show_counter_orig = show_counter
    print('swirl')
    for x in swirl_lights[0]:
        pixels.clear()
        pixels.set_pixel(x, colorDict['green'])
        pixels.show()
        time.sleep(0.075)
        if show_counter_orig != show_counter:
            return
        
    for x in swirl_lights[1]:
        pixels.clear()
        pixels.set_pixel(x, colorDict['yellow'])
        pixels.show()
        time.sleep(0.075)
        if show_counter_orig != show_counter:
            return
        
    for x in swirl_lights[2]:
        pixels.clear()
        pixels.set_pixel(x, colorDict['red'])
        pixels.show()
        time.sleep(0.075)
        if show_counter_orig != show_counter:
            return
        
def shift_gradient():
    global show_counter
    show_counter_orig = show_counter
    print('shift_gradient')
    pixels.set_pixel_line_gradient(0, numpix-1, colorDict['red'], colorDict['green'])
    for x in range(numpix):
        pixels.rotate_right()
        pixels.show()
        time.sleep(0.1)
        if show_counter_orig != show_counter:
            return
        
    for x in range(numpix):
        pixels.rotate_left()
        pixels.show()
        time.sleep(0.1)
        if show_counter_orig != show_counter:
            return

def test_strip():
    pixels.clear()
    pixels.set_pixel_line(0, 9, colorDict['green'])
    pixels.set_pixel_line(10, 19, colorDict['yellow'])
    pixels.set_pixel_line(20, 29, colorDict['red'])
    pixels.show()
    
def show_stoplight():
    global show_counter
    show_counter_orig = show_counter
    print('stoplight')
    pixels.clear()
    pixels.set_pixel_line(0, 9, colorDict['green'])
    pixels.show()
    sleep_time = random.randint(5,15)
    for x in range(sleep_time):
        time.sleep(1)    
        if show_counter_orig != show_counter:
            return
    
    pixels.clear()
    pixels.set_pixel_line(10, 19, colorDict['yellow'])
    pixels.show()
    sleep_time = 3
    for x in range(sleep_time):
        time.sleep(1)    
        if show_counter_orig != show_counter:
            return
    
    pixels.clear()
    pixels.set_pixel_line(20, 29, colorDict['red'])
    pixels.show()
    sleep_time = random.randint(5,15)
    for x in range(sleep_time):
        time.sleep(1)    
        if show_counter_orig != show_counter:
            return
    
def party():
    print('party')
    pixels.clear()
    if random.choice([0, 1]):
        pixels.set_pixel_line(0, 9, colorDict['green'])
        
    if random.choice([0, 1]):
        pixels.set_pixel_line(10, 19, colorDict['yellow'])
        
    if random.choice([0, 1]):
        pixels.set_pixel_line(20, 29, colorDict['red'])
    pixels.show()
    time.sleep(0.25)

test_strip()
time.sleep(2)

button.irq(debounce, Pin.IRQ_FALLING, hard=True)

def show_things():
    global show_counter
    if show_counter == 0:
        show_stoplight()
    elif show_counter == 1:
        party()
    elif show_counter == 2:
        val = random.randint(0, 101)
        for x in range(random.randint(1, 2)):
            if val < 33:
                swirl()
            elif val <= 66:
                shift_gradient()
            elif val <= 100:
                shimmer()
                
    else:
        show_counter = 0
        show_stoplight
        
while(True):
    show_things()
#     show_stoplight()


