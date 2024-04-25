from machine import Pin, PWM, Timer
from time import sleep

y_switch = Pin(0, Pin.IN, Pin.PULL_UP)
x_switch = Pin(1, Pin.IN, Pin.PULL_UP)

start_button = Pin(21, Pin.IN, Pin.PULL_UP)
stop_button = Pin(22, Pin.IN, Pin.PULL_UP)
reset_button = Pin(26, Pin.IN, Pin.PULL_UP)
home_button = Pin(27, Pin.IN, Pin.PULL_UP)

dir_pin_y = Pin(12, Pin.OUT)
step_pin_y = Pin(13, Pin.OUT)
dir_pin_x = Pin(14, Pin.OUT)
step_pin_x = Pin(15, Pin.OUT)

servo_pin = PWM(Pin(17, Pin.OUT))

step_pin_x.value(0)
step_pin_y.value(0)
y_count = 0
x_count = 0
servo_pin.freq(50)
def do():
    global x_count
    global y_count
    file = open("demo.txt", "r")
    lines = file.readlines()
    for line in lines:
        prefix = line[0]
        value = line.lstrip(prefix)
        if prefix == "H":
            if int(value) == 1:
                head("down")
            elif int(value) == 0:
                head("up")
        if prefix == "G":
            x_value = int(value.rsplit(",")[0])
            y_value = int(value.rsplit(",")[1])
            dirX = "+"
            dirY = "+"
            if x_value < 0:
                dirX = "-"
            if y_value < 0:
                dirY = "-"
            if x_value == y_value:
                for i in range(y_value):
                    if stop_button.value() == 1:  
                        step("y", dirY)
                        step("x", dirX)
                        sleep(1/400)
                    else:
                        while start_button.value() == 1:
                            sleep(.25)
                            if reset_button.value() == 0:
                                standby()      
            else:
                if x_value > y_value:
                    relative_step = abs(y_value/x_value)
                    cumulative_step = 0
                    for i in range(x_value):
                        if stop_button.value() == 1:
                            step("x",dirX)
                            cumulative_step += relative_step
                            if cumulative_step >= 1:
                                step("y",dirY)
                                cumulative_step = cumulative_step - 1
                            sleep(1/400)
                        else:
                            while start_button.value() == 1:
                                sleep(.25)
                                if reset_button.value() == 0:
                                    standby()
                else:
                    relative_step = abs(x_value/y_value)
                    cumulative_step = 0
                    for i in range(y_value):
                        if stop_button.value() == 1:
                            step("y",dirY)
                            cumulative_step += relative_step
                            if cumulative_step >= 1:
                                step("x",dirX)
                                cumulative_step = cumulative_step - 1
                            sleep(1/400)
                        else:
                            while start_button.value() == 1:
                                sleep(.25)
                                if reset_button.value() == 0:
                                    standby()
    kalib()
    standby()

def standby():
    while start_button.value() == 1:
        if home_button.value() == 0:
                kalib()
    do()

def head(dir):
    if dir == "down":
        servo_pin.duty_ns(2300000)
        sleep(0.1)
    elif dir == "up":
         servo_pin.duty_ns(2560000)
         sleep(0.1)

def step(axis, dir):
    global dir_pin_y
    global step_pin_y
    global dir_pin_x
    global step_pin_x
    if axis == "y":
        if dir == "+":
            dir_pin_y.value(0)
        elif dir == "-":
            dir_pin_y.value(1)
        step_pin_y.value(1)
        step_pin_y.value(0)
    elif axis == "x":
        if dir == "+":
            dir_pin_x.value(0)
        elif dir == "-":
            dir_pin_x.value(1)
        step_pin_x.value(1)
        step_pin_x.value(0)
        
def kalib():
    head("up")
    dir_pin_y.value(1)
    dir_pin_x.value(1)
    while y_switch.value() == 1:
        global y_count
        step_pin_y.value(1)
        step_pin_y.value(0)
        y_count = y_count + 1
        sleep(1/450)
    y_count = 0
    while x_switch.value() == 1:
        global x_count
        step_pin_x.value(1)
        step_pin_x.value(0)
        x_count = x_count + 1
        sleep(1/450)
    x_count = 0
    standby()

sleep(0.5)
standby()