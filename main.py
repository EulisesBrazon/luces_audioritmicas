from ST7735 import TFT
from machine import SPI,Pin,PWM, UART
from neopixel import Neopixel
from sysfont import sysfont
import _thread
from machine import ADC
#from machine import Timer
import random
from utime import sleep,sleep_ms
#concurrencia
import uasyncio as asyncio

brillo = 20

velocidad = 13500 #frecuencia adecuada
bt = machine.UART(1, baudrate=velocidad, bits=8, parity=1, stop=1, tx=machine.Pin(8), rx=machine.Pin(9))
#bt = UART(1, velocidad)
bt.init(velocidad, bits=8, parity=1, stop=1)
microphone = ADC(26)#input signal microphone
base = 22 #number of led in the base of the struct
numPixel = 52

#datos pantalla
size = 4
separation = 4
opcion = 0

gRed = 255
gGreen = 0
gBlue = 0

strip = Neopixel(numPixel, 0, 15, "GRB")#num_leds, state_machine, pinGPIO, mode="RGB"\
strip.brightness(brillo)#overall brightness (0-255)

#declaration for the use of the screen
spi = SPI(0, baudrate=20000000, polarity=0, phase=0, sck=Pin(2), mosi=Pin(3), miso=Pin(4))
tft=TFT(spi,0,7,1)
tft.initr()
tft.rgb(True)

delay = 0
efecto = 0

red = (255, 0, 0)
orange = (255, 50, 0)
yellow = (255, 100, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
indigo = (100, 0, 90)
violet = (200, 0, 100)
colors_rgb = [red, orange, yellow, green, blue, indigo, violet]


testDispley_thread = False
rainbowEffect_thread = False

dictionary = [ 	[b'\x15','q','Q'],
                [b'\x1d','w','W'],
                [b'$','e','E'],
                [b'-','r','R'],
                [b',','t','T'],
                [b'5','y','Y'],
                [b'<','u','U'],
                [b'C','i','I'],
                [b'D','o','O'],
                [b'M','p','P'],
                [b'\x1c','a','A'],
                [b'\x1b','s','S'],
                [b'#','d','D'],
                [b'+','f','F'],
                [b'4','g','G'],
                [b'3','h','H'],
                [b';','j','J'],
                [b'B','k','K'],
                [b'K','l','L'],
                [b'\x1a','z','Z'],
                [b'"','x','X'],
                [b'!','c','C'],
                [b'*','v','V'],
                [b'2','b','B'],
                [b'1','n','N'],
                [b':','m','M'],
                [b')',' ',' '],
                [b'\x16','1',''],
                [b'\x1e','2',''],
                [b'&','3',''],
                [b'%','4',''],
                [b'.','5',''],
                [b'6','6',''],
                [b'=','7',''],
                [b'>','8',''],
                [b'F','9',''],
                [b'E','0','']]

old_data = ''
new_data = ''
keyRelease_flag = False
shift_flag = False

def getKeyboard():
    global old_data
    global new_data
    global keyRelease_flag
    global shift_flag
    if bt.any() > 0 :
        code = bt.read(1)
        #print(code)
        if (code == b'\xf0'): #stopped pressing the key
            keyRelease_flag = True
        else:   
            if (code == b'\x12'): # code for shift 
                if (keyRelease_flag):
                    shift_flag = False
                    keyRelease_flag = False
                else:
                    shift_flag = True
            else:
                
                old_data = new_data
                new_data = code
                
                if keyRelease_flag:
                    if old_data==new_data:
                        keyRelease_flag = False
                    else:
                        #print('error')
                        keyRelease_flag = False
                else:
                    if shift_flag:
                        for word in dictionary:
                            if code == word[0]:
                                return word[2]
                                break
                        if (code == b'u'): #flcha hacia arriba
                                return b'u'
                        elif (code == b'r'): #flcha hacia abajo
                            return b'r'
                        elif (code == b't'): #flcha hacia arriba
                            return b't'
                        elif (code == b'k'): #flcha hacia abajo
                            return b'k'
                    else:
                        for word in dictionary:
                            if code == word[0]:
                                return word[1]
                                #shift_flag = True
                                break
                        if (code == b'u'): #flcha hacia arriba
                                return b'u'
                        elif (code == b'r'): #flcha hacia abajo
                            return b'r'
                        elif (code == b't'): #flcha hacia arriba
                            return b't'
                        elif (code == b'k'): #flcha hacia abajo
                            return b'k'
        

def rainbowEffect():
    global delay
    red = 255
    green = 0
    blue = 0
    for i in range(255):
        strip.set_pixel(0,(red,green,blue))
        strip.rotate_right()
        strip.show()
        red = red - 1
        green = green + 1
        sleep_ms(delay)
   
    for i in range(255):
        strip.set_pixel(0,(red,green,blue))
        strip.rotate_right()
        strip.show()
        green = green - 1
        blue = blue + 1
        sleep_ms(delay)

    for i in range(255):
        strip.set_pixel(0,(red,green,blue))
        strip.rotate_right()
        strip.show()
        blue = blue - 1
        red = red + 1    
        sleep_ms(delay)
        #await asyncio.sleep_ms(0.1)
            
def red_to_green(delay):
    red = 255
    green = 0
    for i in range(255):
        strip.fill((red,green,0))
        strip.show()
        print(i)
        #sleep(delay)
        red = red - 1
        green = green + 1
    
def mostrar_temperatura():
    temp = machine.ADC(4)
    conversion_factor = 3.3 / (65535)
    reading = temp.read_u16() * conversion_factor
    temperatura = 27 - (reading - 0.706)/0.001721
    print("Temperatura interna: {:.2f}°C".format(temperatura))

def rainbowEffect1():
    for colour in colors_rgb:
        for position in range(numPixel):
            strip.set_pixel(position,(colour))
            strip.show()
            sleep_ms(delay)
            
def barEffect(value,colour, background): #in progress are bug
    value = value - base
    if value > 1:
        for position in range(base):
            strip.set_pixel(position,colour)
            
    for position in range(value):
        strip.set_pixel(base + position, colour)
    strip.show()
    
    for i in range(value):
        strip.set_pixel( base - 2 + (value - i), background)
        strip.show()
        sleep_ms(delay)
    
    if value > 1:
        for position in range(base):
            strip.set_pixel(position,background)
        strip.show()
    
    
    
            

def microphoneSignal(t):
    try:
        intencidad = rescale(microphone.read_u16(),27500,35000,0,255)
        strip.fill((intencidad,0,0))
        strip.show()
    except:
        print("An exception occurred")
        
#tim=machine.Timer()  
#tim.init(mode=Timer.PERIODIC, freq=20000, callback=microphoneSignal)


def testlines(color):
    tft.fill(TFT.BLACK)
    for x in range(0, tft.size()[0], 6):
        tft.line((0,0),(x, tft.size()[1] - 1), color)
    for y in range(0, tft.size()[1], 6):
        tft.line((0,0),(tft.size()[0] - 1, y), color)

    tft.fill(TFT.BLACK)
    for x in range(0, tft.size()[0], 6):
        tft.line((tft.size()[0] - 1, 0), (x, tft.size()[1] - 1), color)
    for y in range(0, tft.size()[1], 6):
        tft.line((tft.size()[0] - 1, 0), (0, y), color)

    tft.fill(TFT.BLACK)
    for x in range(0, tft.size()[0], 6):
        tft.line((0, tft.size()[1] - 1), (x, 0), color)
    for y in range(0, tft.size()[1], 6):
        tft.line((0, tft.size()[1] - 1), (tft.size()[0] - 1,y), color)

    tft.fill(TFT.BLACK)
    for x in range(0, tft.size()[0], 6):
        tft.line((tft.size()[0] - 1, tft.size()[1] - 1), (x, 0), color)
    for y in range(0, tft.size()[1], 6):
        tft.line((tft.size()[0] - 1, tft.size()[1] - 1), (0, y), color)
        
def rescale(signal, in_min, in_max, out_min, out_max):
        if(signal <  in_min):
            return out_min
        if(signal >  in_max):
            return out_max
        return int((signal - in_min)*(out_max - out_min)/(in_max - in_min) + out_min)
    
    

def testDispley():
    while True: #not testDispley_thread:
        testlines(TFT.RED)
        #await asyncio.sleep_ms(0.1)
        testlines(TFT.MAROON)
        #await asyncio.sleep_ms(0.1)
        testlines(TFT.GREEN)
        #await asyncio.sleep_ms(0.1)
        testlines(TFT.FOREST)
        testlines(TFT.BLUE)
        testlines(TFT.NAVY)
        testlines(TFT.CYAN)
        testlines(TFT.YELLOW)
        testlines(TFT.PURPLE)
        testlines(TFT.GRAY)
        testlines(TFT.WHITE)
        #await asyncio.sleep_ms(0.1)
        
#tft.fill(TFT.RED)
def displey():
    while True:
        testDispley()

def controlThrteat():
    loop = asyncio.get_event_loop()
    loop.create_task(testDispley())
    loop.create_task(rainbowEffect(3))
    
    loop.run_forever()
    
def chageOption(entero):
    global opcion
    opcion = opcion + entero
    maximo = 6#numero de opciones
    if opcion < 0:
        opcion = maximo
    elif opcion > maximo:
        opcion = 0
        
def parpadeo():
    global gRed
    global gGreen
    global gBlue
    print(microphone.read_u16())
    intencidad = rescale(microphone.read_u16(),28000,35000,0,100)
    strip.fill((gRed,gGreen,gBlue))
    strip.brightness(int(intencidad))
    strip.show()
    
def menuPrincipal():
    global opcion
    global efecto
    global delay
    global gRed
    global gGreen
    global gBlue
    global brillo 
    old_opcion = 1
    tft.fill(TFT.BLACK)#clean screen
    tft.text((20, 50), 'Hola', TFT.GREEN, sysfont, size, nowrap=True)
    while True:
        tecla = getKeyboard()
        
        if tecla is not  None:
            print(tecla)
            #opcion = str(tecla)
            if tecla == b't':#derecha
                chageOption(1)
                pass
            elif tecla == b'k':#izquierda
                chageOption(-1) 
                pass
            
            if opcion == 0:
                #menuRainbowEffect()
                tft.fill(TFT.BLACK)#clean screen
                tft.text((35, 0), 'Test', TFT.RED, sysfont, 3, nowrap=True)
                tft.text((10, 30), 'Teclado', TFT.RED, sysfont, 3, nowrap=True)
                tft.text((50, 70), str(tecla), TFT.RED, sysfont, 4, nowrap=True)
            elif opcion == 1:
                tft.fill(TFT.BLACK)#clean screen
                tft.text((15, 30), 'Brillo', TFT.RED, sysfont, 3, nowrap=True)
                if tecla == b'u':#arriba
                    if brillo == 100:
                        pass
                    else:
                        brillo = brillo + 10
                        strip.brightness(brillo)
                elif tecla == b'r':#abajo
                    if brillo == 10:
                        pass
                    else:
                        brillo = brillo - 10
                        strip.brightness(brillo)
                tft.text((55, 60), str(brillo), TFT.RED, sysfont, 3, nowrap=True)
            elif opcion == 2:
                tft.fill(TFT.BLACK)#clean screen
                tft.text((9, 30), 'Rainbow', TFT.RED, sysfont, 3, nowrap=True)
                if tecla == b'u':#arriba
                    if delay == 50:
                        pass
                    else:
                        delay = delay + 5
                elif tecla == b'r':#abajo
                    if delay == 0:
                        pass
                    else:
                        delay = delay - 5
                tft.text((55, 60), str(delay), TFT.RED, sysfont, 3, nowrap=True)
            elif opcion == 3:
                tft.fill(TFT.BLACK)#clean screen
                tft.text((9, 30), 'Efectos', TFT.RED, sysfont, 3, nowrap=True)
                if tecla == b'u':#arriba
                    efecto = 0
                elif tecla == b'r':#abajo
                    efecto = 1
                if efecto == 0:
                    tft.text((9, 60), 'Rainbow', TFT.GREEN, sysfont, 3, nowrap=True)
                elif efecto ==1:
                    tft.text((10, 60), 'Audioritmo', TFT.GREEN, sysfont, 2, nowrap=True)
            elif opcion == 4:
                tft.fill(TFT.BLACK)#clean screen
                tft.text((9, 30), 'Colores', TFT.YELLOW, sysfont, 3, nowrap=True)
                tft.text((30, 60), 'R', TFT.RED, sysfont, 3, nowrap=True)
                tft.text((60, 60), 'G', TFT.GREEN, sysfont, 3, nowrap=True)
                tft.text((90, 60), 'B', TFT.BLUE, sysfont, 3, nowrap=True)
                if tecla == b'u':#arriba
                    if gRed == 255:
                        pass
                    else:
                        gRed = gRed + 15
                elif tecla == b'r':#abajo
                    if gRed == 0:
                        pass
                    else:
                        gRed = gRed - 15
                tft.text((50, 90), str(gRed), TFT.RED, sysfont, 3, nowrap=True)
            elif opcion == 5:
                tft.fill(TFT.BLACK)#clean screen
                tft.text((9, 30), 'Colores', TFT.YELLOW, sysfont, 3, nowrap=True)
                tft.text((30, 60), 'R', TFT.RED, sysfont, 3, nowrap=True)
                tft.text((60, 60), 'G', TFT.GREEN, sysfont, 3, nowrap=True)
                tft.text((90, 60), 'B', TFT.BLUE, sysfont, 3, nowrap=True)
                if tecla == b'u':#arriba
                    if gGreen == 255:
                        pass
                    else:
                        gGreen = gGreen + 15
                elif tecla == b'r':#abajo
                    if gGreen == 0:
                        pass
                    else:
                        gGreen = gGreen - 15
                tft.text((50, 90), str(gGreen), TFT.GREEN, sysfont, 3, nowrap=True)
            elif opcion == 6:
                tft.fill(TFT.BLACK)#clean screen
                tft.text((9, 30), 'Colores', TFT.YELLOW, sysfont, 3, nowrap=True)
                tft.text((30, 60), 'R', TFT.RED, sysfont, 3, nowrap=True)
                tft.text((60, 60), 'G', TFT.GREEN, sysfont, 3, nowrap=True)
                tft.text((90, 60), 'B', TFT.BLUE, sysfont, 3, nowrap=True)
                if tecla == b'u':#arriba
                    if gBlue == 255:
                        pass
                    else:
                        gBlue = gBlue + 15
                elif tecla == b'r':#abajo
                    if gBlue == 0:
                        pass
                    else:
                        gBlue = gBlue - 15
                tft.text((50, 90), str(gBlue), TFT.BLUE, sysfont, 3, nowrap=True)
                
                
            #elif opcion == 2:
                #testlines(TFT.RED)


        #old_tecla = tecla  
                

            
            #data reading
            
            #h += sysfont["Height"]*size+separation
            #tft.text((0, h), str(ip), TFT.GREEN, sysfont, size, nowrap=True)
            #h += sysfont["Height"]*size+separation
            #sleep(0.5)
        
        
def concurrencia():
    global efecto
    if efecto == 0:
        rainbowEffect()
    elif efecto == 1:
        parpadeo()
    

def main():
    while True :
        try:
            concurrencia()
            #mostrar_temperatura()
        except Exception as e:
            print("Error:", e)
        #sleep(2)
        
_thread.start_new_thread(menuPrincipal, ())
        
if __name__ == '__main__':
    main()                                                                                                        