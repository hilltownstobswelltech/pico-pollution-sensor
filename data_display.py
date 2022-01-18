import picounicorn as uni
import random
import time
import utime
import uselect
from machine import UART

uart = UART(0, 9600)
# uart.init(9600,8,None,1)

characters = {
    

    "0" :
        [
            [000,000,000],
            [255,255,255],
            [255,000,255],
            [255,000,255],
            [255,000,255],
            [255,255,255]
        ],
    
    "1" :
        [
            [000,000,000],
            [000,255,000],
            [000,255,000],
            [000,255,000],
            [000,255,000],
            [000,255,000]
        ],
    
    "2" :
        [
            [000,000,000],
            [255,255,255],
            [000,000,255],
            [255,255,255],
            [255,000,000],
            [255,255,255]
        ],
    
    "3" :
        [
            [000,000,000],
            [255,255,255],
            [000,000,255],
            [255,255,255],
            [000,000,255],
            [255,255,255]
        ],
    
    "4" :
        [
            [000,000,000],
            [255,000,255],
            [255,000,255],
            [255,255,255],
            [000,000,255],
            [000,000,255]
        ],
    
    "5" :
        [
            [000,000,000],
            [255,255,255],
            [255,000,000],
            [255,255,255],
            [000,000,255],
            [255,255,255]
        ],
    
    "6" :
        [
            [000,000,000],
            [255,255,255],
            [255,000,000],
            [255,255,255],
            [255,000,255],
            [255,255,255]
        ],
    
    "7" :
        [
            [000,000,000],
            [255,255,255],
            [000,000,255],
            [000,255,000],
            [000,255,000],
            [000,255,000]
        ],
    
    "8" :
        [
            [000,000,000],
            [255,255,255],
            [255,000,255],
            [255,255,255],
            [255,000,255],
            [255,255,255]
        ],
    
    "9" :
        [
            [000,000,000],
            [255,255,255],
            [255,000,255],
            [255,255,255],
            [000,000,255],
            [000,000,255]
        ],
    ".":
        [
            [000],
            [000],
            [000],
            [000],
            [255],
            [000]
        ],
    "P":
        [
            [255,255,255],
            [255,000,255],
            [255,255,255],
            [255,000,000],
            [255,000,000],
            [000,000,000],
        ],
    "M":
            [
            [000,000,000,000,000],
            [000,000,000,000,000],
            [000,000,000,000,000],
            [255,000,000,000,255],
            [255,255,000,255,255],
            [255,000,255,000,255],
            [255,000,000,000,255],

        ],
    
    "O":
        [
            [000,000,000],
            [255,255,255],
            [255,000,255],
            [255,000,255],
            [255,000,255],
            [255,255,255],
            [000,000,000],
        ],
    
    "L":
        [
            [000,000,000],
            [255,000,000],
            [255,000,000],
            [255,000,000],
            [255,000,000],
            [255,255,255],
        ],
    
    "!":
        [
            [000,000,000],
            [000,255,000],
            [000,255,000],
            [000,255,000],
            [000,000,000],
            [000,255,000],
        ],
    
    "N":
        [
            [000,000,000,000,000],
            [255,000,000,000,255],
            [255,255,000,000,255],
            [255,000,255,000,255],
            [255,000,000,255,255],
            [255,000,000,000,255],
        ],
    
    "D":
        [
            [000,000,000],
            [255,255,000],
            [255,000,255],
            [255,000,255],
            [255,000,255],
            [255,255,000],
        ],
    "-":
        [
            [000,000,000],
            [000,000,000],
            [000,000,000],
            [255,255,255],
            [000,000,000],
            [000,000,000],
        ],
    
    }


uni.init()

w = uni.get_width()
h = uni.get_height()

brightness = 0.5

def export_to_leds(cells):
    for x in range(w):
        for y in range(h):
            value = cells.get_cell(x,y)
            if type(value) != list:
                uni.set_pixel_value(x,y,value)
            else:
                uni.set_pixel(x,y,value[0],value[1],value[2])

class Cells:
    def __init__(self):
        self.cells = [[0]*h for i in range(w)]

    def clear_all(self):
        for x in range(w):
            for y in range(h):
                self.cells[x][y] = 0
    def set_cell(self,x,y,r,g=None,b=None):
        if g==None or b==None:
            self.cells[x][y] = r
        else:
            self.cells[x][y] = [r,g,b]
    def get_cell(self,x,y):
        return self.cells[x][y]

cells_A = Cells()
cells_A.clear_all()

def assign_letter(cells, letter, y_offset=0, colour=None): # (screen is sideways)
    for x in range(len(characters[letter])):
        for y in range(len(characters[letter][x])):
            if colour == "red":
                cells.set_cell(y+y_offset,x,int(characters[letter][x][y]*brightness),0,0)
            elif colour == "green":
                cells.set_cell(y+y_offset,x,0,int(characters[letter][x][y]*brightness*0.75),0)
            elif colour == "blue":
                cells.set_cell(y+y_offset,x,0,0,int(characters[letter][x][y]*brightness))
            else:
                cells.set_cell(y+y_offset,x,int(characters[letter][x][y]*brightness*0.75))

def pm2_5_label(cells, _=None):

    assign_letter(cells,"P",0, "red")
    assign_letter(cells,"M",3, "green")
    assign_letter(cells,"2",9, "red")
    assign_letter(cells,".",12, "blue")
    assign_letter(cells,"5",13, "green")

def pm10_label(cells, _=None):

    assign_letter(cells,"P",0, "red")
    assign_letter(cells,"M",3, "green")
    assign_letter(cells,"1",9, "red")
    assign_letter(cells,"0",12, "red")

def over_level_label(cells):
    
    assign_letter(cells,"O",3, "red")
    assign_letter(cells,"L",7, "red")
    assign_letter(cells,"!",10, "red")
    
def no_data_label(cells):
    
    assign_letter(cells,"N",2, "red")
    assign_letter(cells,"D",8, "red")
    assign_letter(cells,"!",11, "red") 


def num_display(cells, num):
    if num == None:
        no_data_label(cells)
    elif num > 9999.9999999 or num < -999.99999999:
        over_level_label(cells)
    elif num <= 9999.9999999 and num > 999.99999999 or num >= -999.999999 and num < -99.9999999:
        # zero DP
        if num < 0:
            num = "{:.3f}".format(num)
            assign_letter(cells,"-",1, "blue")
            assign_letter(cells,num[1],5, "red")
            assign_letter(cells,num[2],9, "red")
            assign_letter(cells,num[3],13, "red")
        else:
            num = "{:.3f}".format(num)
            assign_letter(cells,num[0],1, "red")
            assign_letter(cells,num[1],5, "red")
            assign_letter(cells,num[2],9, "red")
            assign_letter(cells,num[3],13, "red")
    elif num <= 999.999 and num > 99.9999 or num >= -99.99999999 and num < -9.99999999:
        # one DP only
        if num < 0:
            num = "{:.3f}".format(num)
            assign_letter(cells,"-",1, "blue")
            assign_letter(cells,num[1],5, "red")
            assign_letter(cells,num[2],9, "red")
            assign_letter(cells,".",12, "blue")
            assign_letter(cells,num[4],13, "green")
        else:
            num = "{:.3f}".format(num)
            assign_letter(cells,num[0],1, "red")
            assign_letter(cells,num[1],5, "red")
            assign_letter(cells,num[2],9, "red")
            assign_letter(cells,".",12, "blue")
            assign_letter(cells,num[4],13, "green")
            
    elif num <= 99.99999999 and num > 9.99999999 or num >= -9.999999999 and num < -0.9999999999:
        # two DP
        if num < 0:
            num = "{:.3f}".format(num)
            assign_letter(cells,"-",1, "blue")
            assign_letter(cells,num[1],5, "red")
            assign_letter(cells,".",8, "blue")
            assign_letter(cells,num[3],9, "green")
            assign_letter(cells,num[4],13, "green")
        else:
            num = "{:.3f}".format(num)
            assign_letter(cells,num[0],1, "red")
            assign_letter(cells,num[1],5, "red")
            assign_letter(cells,".",8, "blue")
            assign_letter(cells,num[3],9, "green")
            assign_letter(cells,num[4],13, "green")
    else:
        # three DP
        if num < 0:
            num = "{:.3f}".format(num)
            assign_letter(cells,"-",1, "blue")
            assign_letter(cells,num[1],5, "red")
            assign_letter(cells,".",8, "blue")
            assign_letter(cells,num[3],9, "green")
            assign_letter(cells,num[4],13, "green")
        else:
            num = "{:.3f}".format(num)
            assign_letter(cells,num[0],1, "red")
            assign_letter(cells,".",4, "blue")
            assign_letter(cells,num[2],5, "green")
            assign_letter(cells,num[3],9, "green")
            assign_letter(cells,num[4],13, "green")
    
display_cell = Cells()
data = None
display_funcs = [pm2_5_label, num_display, pm10_label, num_display]
display_counter = 0
good_data = [None,None]  # PM2.5, PM10
last_change = utime.ticks_ms()
transmission = ""
while True:


    character = uart.read()
    while character is not None:
        character = character.decode()
        if character != "\n":
            transmission += character
        character = uart.read()
    if transmission != "":
        print(transmission)
        transmission = transmission[:-1].split("@")
        print(transmission)
        good_data[0] = float(transmission[0])
        good_data[1] = float(transmission[1])
    transmission = ""
        
    if utime.ticks_diff(utime.ticks_ms(), last_change) > 1000:
        display_cell.clear_all()
        print("display advance")
        num = None
        last_change = utime.ticks_ms()
        if display_counter == 1:
            num = good_data[0] # PM2.5
        if display_counter == 3:
            num = good_data[1] # PM10
        display_funcs[display_counter](display_cell, num)
        export_to_leds(display_cell)
        
        display_counter +=1
        if display_counter > 3:
            display_counter = 0

