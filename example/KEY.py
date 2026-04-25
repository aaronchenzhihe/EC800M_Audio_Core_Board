from machine import Pin,ExtInt
import utime

gpio = Pin(Pin.GPIO27, Pin.OUT, Pin.PULL_DISABLE, 0)

def fun(args):
    args[1]=gpio.read() # 读取GPIO电平状态
    print('### interrupt  {} ###'.format(args)) # args[0]:gpio号 args[1]:上升沿或下降沿
    

extint = ExtInt(ExtInt.GPIO27, ExtInt.IRQ_RISING, ExtInt.PULL_PU, fun,filter_time=50)#使能滤波，滤波时间为50ms
extint.enable()