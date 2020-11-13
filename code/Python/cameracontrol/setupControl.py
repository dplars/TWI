import serial
import time
import sys
import cv2
import os
from matplotlib import pyplot

# insert batch of plate number eg: 04
batchnumber= 4
bnr = '{:03d}'.format(batchnumber)

print(serial.__version__)

ser = serial.Serial('/dev/cu.usbserial-14620', 9600, timeout=0.5)       # change port according to arduino script
print(ser.name)

# initialize camera
cap = cv2.VideoCapture(1)
timedelay = 0.15   # wait for arduino to do things  -> better to long than to short --> time for putting new plates on takes longer
turnwaitfactor = 10  # how many times to wait the timedelay for the picture

def change_leds():
    ser.write(b'alloff')
    time.sleep(timedelay)
    ser.write(b'brightness70')
    time.sleep(timedelay)
    start = 4
    end = 10
    # turn leds on
    for i in range(start,end):
        turn_led_on(i, 'A')
        turn_led_on(i, 'B')

    time.sleep(3*timedelay)
    for i in range(start,end):
        turn_led_off(i, 'A')
        turn_led_off(i, 'B')

def set_brightness(b):
    time.sleep(timedelay)
    brightness = 'brightness'+str(b)
    ser.write(brightness.encode())
    time.sleep(timedelay)


def all_led_off():
    time.sleep(timedelay)
    led = 'alloff'
    ser.write(led.encode())
    time.sleep(timedelay)

def all_led_on():
    time.sleep(timedelay)
    led = 'allon'
    ser.write(led.encode())
    time.sleep(timedelay)


def turn_led_on(index, strip=None):
    time.sleep(timedelay)
    if strip is None:
        schrijf = 'nrleds+' + str(index)
    else:
        schrijf = 'nrled+'+ strip + str(index)
    ser.write(schrijf.encode())
    time.sleep(timedelay)


def turn_led_off(index, strip=None):
    time.sleep(timedelay)
    if strip is None:
        schrijf = 'nrleds-' + str(index)
    else:
        schrijf = 'nrled-'+ strip + str(index)
    ser.write(schrijf.encode())
    time.sleep(timedelay)


def step_forward():
    time.sleep(timedelay)
    schrijf = "step+160"
    ser.write(schrijf.encode())
    time.sleep(timedelay*turnwaitfactor)     # give time to turn

def step_back():
    time.sleep(timedelay)
    schrijf = "step-160"
    ser.write(schrijf.encode())
    time.sleep(timedelay*5)     # give time to turn

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

def run():

    # increase brightness
    set_brightness(70)

    #default images directory
    images_dir = '/Users/larsdepauw/Documents/Lars.nosync/Documents/School/1Ma ing/Masterproef/TWI/code/Python/cameracontrol/images/'

    for plaatje in range(1,6):

        # create formatting for plate number
        pnr = '{:03d}'.format(plaatje)

        # create savedir
        save_dir = images_dir + 'batch_' + bnr + '_plate_' + '{:03d}'.format(plaatje) + '/'

        # create dir to save files
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)


        # take picture with full lighting
        all_led_on()
        take_picture(images_dir+'b_'+bnr+'_p_'+pnr+'_l_000.png')  # save white picture as 000
        all_led_off()

        for light in range(0,15):

            # create formatting for light number
            lnr = '{:03d}'.format(light)
            # turn leds on
            turn_led_on(light)

            # create url
            url = save_dir+'b_'+bnr+'_p_'+pnr+'_l_'+lnr+'.png'
            print(url)

            # save picture of current state
            #take_picture(url)

            # turn leds off again
            turn_led_off(light)

        #step to next plate
        step_back()

    # clean up: turn back to first plate
    to_start()
    cv2.destroyAllWindows()     # clean up windows


#turn all leds of
all_led_off()

# show change leds to say it is done
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
    else:
        print(schrijf)
        ser.write(schrijf.encode())


ser.close()
cap.release()
cv2.destroyAllWindows()

