import serial
import time
import sys
import cv2
import os
from matplotlib import pyplot

# insert batch of plate number eg: 04
batchnumbers = [1,2]


print(serial.__version__)

ser = serial.Serial('/dev/cu.usbserial-14620', 9600, timeout=0.5)       # change port according to arduino script
print(ser.name)

# initialize camera
cap = cv2.VideoCapture(1)
timedelay = 0.20   # wait for arduino to do things  -> better to long than to short --> time for putting new plates on takes longer
turnwaitfactor = 10  # how many times to wait the timedelay for the picture

#colors = ["white", "red", "blue", "green"]
colors = ["white", "red"]
#strips = ["A", "B"]
strips = [None]
bullet = 'nb' # b of nb says bullet or no bullet

# enter start led
startled = 6
# enter stopled
stopled = 11

def change_leds():
    ser.write(b'alloff')
    time.sleep(timedelay)
    ser.write(b'brightness90')
    time.sleep(timedelay)
    #start = 4
    #end = 10
    # turn leds on
    for i in range(startled,stopled):
        turn_led_on(i, 'A')
        turn_led_on(i, 'B')

    time.sleep(3*timedelay)
    for i in range(startled,stopled):
        turn_led_off(i, 'A')
        turn_led_off(i, 'B')

def set_brightness(b):
    time.sleep(timedelay)
    brightness = 'brightness'+str(b)+'/'
    ser.write(brightness.encode())
    time.sleep(timedelay)


def all_led_off():
    print("all leds off")
    time.sleep(timedelay)
    led = 'alloff/'
    ser.write(led.encode())
    time.sleep(timedelay)

def all_led_on():
    print("all led on")
    time.sleep(timedelay)
    led = 'allon/'
    ser.write(led.encode())
    time.sleep(timedelay)

def leds_on(start, stop):
    for i in range(start, stop+1):
        turn_led_on(i)

def turn_led_on(index, strip=None):
    time.sleep(timedelay)
    if strip is None:
        schrijf = 'nrleds+' + str(index)+'/'
    else:
        schrijf = 'nrled+'+ strip + str(index)+'/'
    ser.write(schrijf.encode())
    time.sleep(timedelay)


def turn_led_off(index, strip=None):
    time.sleep(timedelay)
    if strip is None:
        schrijf = 'nrleds-' + str(index)+'/'
    else:
        schrijf = 'nrled-'+ strip + str(index)+'/'
    ser.write(schrijf.encode())
    time.sleep(timedelay)


def step_forward():
    time.sleep(timedelay)
    schrijf = "step+160/"
    ser.write(schrijf.encode())
    time.sleep(timedelay*turnwaitfactor)     # give time to turn

def step_back():
    time.sleep(timedelay)
    schrijf = "step-160/"
    ser.write(schrijf.encode())
    time.sleep(timedelay*turnwaitfactor)     # give time to turn

def set_color(color):
    time.sleep(timedelay)
    schrijf = color+'/'
    ser.write(schrijf.encode())
    time.sleep(timedelay * turnwaitfactor)  # give time to turn

def to_start():
    time.sleep(timedelay)
    for i in range(0,5):
        step_forward()
        time.sleep(timedelay*turnwaitfactor)


def read_camera():
    ret, frame = cap.read()
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
    return frame, rgb


def show_image(image, url='image'):
    cv2.imshow(str(url), image)


def save_frame(url, frame):
    out = cv2.imwrite(str(url), frame)
    return out


def take_picture(url):
    ret, frame = cap.read()
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)

    cv2.imshow('frame', rgb)
    if cv2.waitKey(1):
        out = cv2.imwrite(url, frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        return -1

def scroll_plates(dir):
    for i in range(0,20):
        if dir == 1:
            step_forward()
        else:
            step_back()

def run():

    index = 0
    while (True):
        get = int(input('give batch '+str(index)+' number: '))
        if get == 0:
            break
        batchnumbers[index] = get
        index += 1

    print("batchnummers: "+str(batchnumbers))

    bullet = input('give b for bullet, nb for no bullet: ')

    print("batch: "+str(batchnumbers[0])+" batch: "+str(batchnumbers[1])+" bullet: "+bullet)
    confirm = int(input('confirm these settings: '))
    if confirm != 1:
        return

    # increase brightness
    set_brightness(90)

    #default images directory
    images_dir = '/Users/larsdepauw/Documents/Lars.nosync/Documents/School/1Ma ing/Masterproef/TWI/code/Python/cameracontrol/images/'

    for batch in batchnumbers:
        for plaatje in range(1,11):

            bnr = '{:03d}'.format(batch)
            # create formatting for plate number
            pnr = '{:03d}'.format(plaatje)

            # create savedir
            save_dir = images_dir + 'batch_' + bnr + '_plate_' + '{:03d}'.format(plaatje) + '/'

            # create dir to save files
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)


            # take picture with full lighting
            #all_led_on()
            all_led_off()
            set_color("white")
            leds_on(startled, stopled)
            take_picture(save_dir+'b_'+bnr+'_p_'+pnr+'_l_'+'{:03d}'.format(startled)+'-'+'{:03d}'.format(stopled)+'_white_'+bullet+'.png')  # save white picture as 000
            all_led_off()

            set_color("red")
            leds_on(startled, stopled)
            take_picture(save_dir + 'b_' + bnr + '_p_' + pnr + '_l_'+'{:03d}'.format(startled)+'-'+'{:03d}'.format(stopled)+'_red_' + bullet + '.png')  # save white picture as 000
            all_led_off()

            """for color in colors:
                set_color(color)
                for light in range(startled, stopled):
                    for strip in strips:

                        # create formatting for light number
                        lnr = '{:03d}'.format(light)

                        # turn leds on
                        turn_led_on(light, strip)

                        # create url
                        url = save_dir+'b_'+bnr+'_p_'+pnr+'_'+bullet+'_l_'+lnr+'_'+color+'_'+str(strip)+'.png'
                        print(url)

                        # save picture of current state
                        take_picture(url)

                        # turn leds off again
                        turn_led_off(light)
"""
            #step to next plate if bullet, go the other way round
            if bullet == "b":
                step_forward()
            else:
                step_back()

    # clean up: turn back to first plate
    #to_start()
    cv2.destroyAllWindows()     # clean up windows


#turn all leds of
all_led_off()

# show change leds to say it is done
set_color("white")
change_leds()
while(True):
    print(ser.readline())
    #print('s+2')
    #ser.write(b's+2')
    if 0xFF == ord('q'):
        break
    time.sleep(0.5)
    schrijf = input('geef een commando: ')
    if schrijf == 'q':      # stop program
        break
    if schrijf == 'run':      # run automated picture taking
        run()
    if schrijf == 'tostart':    # return to start
        to_start()
    if schrijf == 'l':  # return to start
        turn_led_on(2)
    if schrijf == 's':
        scroll_plates(1)
    if schrijf == 'b':
        scroll_plates(0)
    else:
        print(schrijf)
        ser.write(schrijf.encode())


ser.close()
cap.release()
cv2.destroyAllWindows()

