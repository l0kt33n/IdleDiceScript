import pyautogui as pag
from time import sleep
from auto import buyallAndRoll,prestige



def loop(l1,l2,l3):
    time=0
    while True:
        #pag.click(l1)
        #pag.click(l2)
        pag.click(l3)
        buyallAndRoll()
        if time%120==0 and time != 0:
            time=0
            prestige()
        else:
        	time += 1
        sleep(1)


l1=(1004,759)
l2=(728,584)
l3=(834,878)

loop(l1,l2,l3)
