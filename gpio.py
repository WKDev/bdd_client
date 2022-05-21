try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")

import random as rd
import time
devs = [23,24,25]
devs_bcm = [16,18,22]


GPIO_INT = 1

def init_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(devs, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(devs_bcm, GPIO.OUT, initial=GPIO.LOW)



def clear_gpio():
    GPIO.output(devs, GPIO.LOW)
    time.sleep(GPIO_INT)


def run_sequential():
    print('sequantial')
    for i in range(1,4):
        rd_dev = rd.choices(devs, k=1)

        GPIO.output(rd_dev, GPIO.HIGH)
        time.sleep(GPIO_INT)
        GPIO.output(rd_dev, GPIO.LOW)
        time.sleep(GPIO_INT)



def run_at_once():
    print('run at once')
    pick_num = rd.choice(range(1,4))

    for i in range(1,4):
        pick_num = rd.choice(range(1,4))
        rd_devs = rd.choices(devs, k=pick_num)

        GPIO.output(rd_devs, GPIO.HIGH)
        time.sleep(GPIO_INT)
        GPIO.output(rd_devs, GPIO.LOW)
        # time.sleep(GPIO_INT)

def exec_ext():
    rnd = rd.random()
    print(rnd)
    if rnd > 0.5:
        run_sequential()
    else:
        run_at_once()




if __name__ == "__main__":
    init_gpio()
    exec_ext()
    # while True:
    #     GPIO.output(23, GPIO.HIGH)
    #     time.sleep(1)
    #     print('off')
    #     GPIO.output(23, GPIO.LOW)
    #     time.sleep(1)

    # run_at_once()






        


    
        
