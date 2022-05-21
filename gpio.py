try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")

import random as rd
import time
devs = [23,24,25]
devs_bcm = [16,18,22]


GPIO_INT = 1000

def init_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(devs, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(devs_bcm, GPIO.OUT, initial=GPIO.LOW)



def clear_gpio():
    for dev in devs:
       GPIO.output(dev, GPIO.LOW)

def run_sequential():
    rd_devs = rd.shuffle(devs)
    for dev in rd_devs:
        GPIO.output(dev, GPIO.HIGH)
        time.sleep(GPIO_INT)
        GPIO.output(dev, GPIO.LOW)


def run_at_once():
    rd_devs = rd.choices(devs, k=rd.choice(range(1,3)))
    for dev in rd_devs:
        GPIO.output(dev, GPIO.HIGH)
        time.sleep(GPIO_INT)

    clear_gpio()

def exec_ext():
    if rd.random() > 0.5:
        run_sequential()
    else:
        run_at_once()




if __name__ == "__main__":
    init_gpio()
    # exec_ext()
    while True:
        GPIO.output(18, GPIO.HIGH)
        time.sleep(300)
        print('off')
        GPIO.output(18, GPIO.LOW)
        time.sleep(300)




        


    
        
