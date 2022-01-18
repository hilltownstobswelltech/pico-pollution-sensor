import utime, binascii
from machine import Pin, ADC, UART, SPI

uart = UART(0, 9600)
# temp_sensor = ADC(4)
# temperature = temp_sensor.read_u16()


sleep = bytearray(19)
wakeup = bytearray(19)
sleep_h = [0xAA, 0xB4, 0x06, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFF, 0xFF, 0x05, 0xAB]
wakeup_h = [0xAA, 0xB4, 0x06, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFF, 0xFF, 0x06, 0xAB]

for i in range(0,len(sleep_h)):
    sleep[i] = int(sleep_h[i])
    wakeup[i] = int(wakeup_h[i])

class time_keeper():
    def __init__(self):
        self.start_time = None
        self.reset()
    def reset(self):
        self.start_time = utime.ticks_ms()
    def elapsed_ms(self):
        t = utime.ticks_diff(utime.ticks_ms(), self.start_time)
        if t < 0:
            t = -1 * t
        return t

timekeeper = time_keeper()

while True:
        if timekeeper.elapsed_ms() > 5 * 1000:
            uart.write(wakeup)
            utime.sleep(5)    
            data = uart.read()
            if data is not None:
                PM25 = (data[3] * 256 + data[2])/10
                PM10 = (data[5] * 256 + data[4])/10
                print("PM25:", PM25,"ug/m3", "PM10:", PM10,"ug/m3")
            utime.sleep(5)
            uart.write(sleep)
            timekeeper.reset()
    
machine.soft_reset()