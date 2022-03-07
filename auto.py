import pyautogui as pag
from time import sleep
from PIL import ImageGrab
import pickle


class Options():
    convertLocation = (1320, 427)
    confirmLocation = (758, 666)
    activateLocation = (841, 420)
    buyOneLocation = (1602, 66)
    buyMaxLocation = (1869, 66)
    buyMaxMode = False
    prestigeWaitTime = 120

def buyallAndRoll():
    pag.press('space')
    pag.press('b')


def prestige():
    pag.press('p')


def checkConvert(options):
    return ImageGrab.grab().getpixel((options.convertLocation)) == (255, 255, 255)


def convert(options):
    pag.click(options.convertLocation)
    sleep(0.5)
    confirm(options)


def confirm(options):
    pag.click(options.confirmLocation)


def switchMode(options):
    if not options.buyMaxMode:
        options.buyMaxMode = True
        pag.click(options.buyMaxLocation)
    else:
        options.buyMaxMode = False
        pag.click(options.buyOneLocation)


def gameLoop(options):
    pag.click(options.activateLocation)
    prestigeTime = 0
    try:
        while True:
            if checkConvert(options):
                convert(options)
                prestigeTime = 0
            else:
                prestigeTime += 1
                if prestigeTime >= options.prestigeWaitTime:
                    prestige()
                    prestigeTime = 0
                if prestigeTime % 5 == 0:
                    switchMode(options)
            buyallAndRoll()
            sleep(1)
    except KeyboardInterrupt:
        print('Program terminated')
        return 0


def setup(options: Options):
    input('Move your mouse to the Convert button and press enter')
    options.convertLocation = getMousePosition()
    input('Move your mouse to the Confirm button and press enter')
    options.confirmLocation = getMousePosition()
    input('Move your mouse to the Activate area and press enter')
    options.activateLocation = getMousePosition()
    input('Move your mouse to the Buy One button and press enter')
    options.buyOneLocation = getMousePosition()
    input('Move your mouse to the Buy Max button and press enter')
    options.buyMaxLocation = getMousePosition()


def getMousePosition():
    return pag.position()


def main():
    pag.FAILSAFE = True
    options = Options()
    try:
        options = pickle.load(file=open('options.p', 'rb'))
    except FileNotFoundError:
        setup(options)
        pickle.dump(options, file=open('options.p', 'wb'))
    gameLoop(options)


if __name__ == '__main__':
    main()
