import cv2
import time
import serial
cap = cv2.VideoCapture(1)

ser = serial.Serial('/dev/cu.usbserial-1460', 9600, timeout=0.5)

def all_led_off():
    time.sleep(1.5)
    led = 'alloff'
    ser.write(led.encode())
    time.sleep(1.5)

def all_led_on():
    time.sleep(1.5)
    led = 'allon'
    ser.write(led.encode())
    time.sleep(1.5)

def take_picture(url):
    ret, frame = cap.read()
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)

    cv2.imshow('frame', rgb)
    if cv2.waitKey(1):
        out = cv2.imwrite(url, frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        return -1

all_led_off()
index = 0
#while(True):

all_led_on()
ret = take_picture('images/test/'+str(index)+'.png')
index += 1
time.sleep(2)

all_led_off()
ret = take_picture('images/test/'+str(index)+'.png')
index += 1
time.sleep(2)


cap.release()
cv2.destroyAllWindows()