from PIL import ImageGrab
from time import sleep, time
import pyautogui as pag
import pickle
import argparse

convertTime = None
fullDeck = False
screenWidth, screenHeight = pag.size()


class UiConfigs():
    def __init__(self):
        self.activateLocation = (841, 420)
        self.buyOneLocation = (1602, 66)
        self.buyMaxLocation = (1869, 66)
        self.buyMaxMode = False
        self.prestigeWaitTime = 120


class FreeStuffConfigs():
    def __init__(self):
        self.activationLocation = (1100, 257)
        self.startLocation = (797, 580)
        self.endLocation = (923, 671)
        self.freeStuffInterVal = 300


class CardsConfigs():
    def __init__(self):
        self.isOpen = False
        self.openLocation = None
        self.closeLocation = None
        self.convertLocation = None
        self.convertConfirmLocation = None


class CasinoConfigs():
    def __init__(self):
        self.openLocation = (1050, 590)
        self.casinoTabLocation = (1050, 590)
        self.investButton = None
        self.closeLocation = None


def buyallAndRoll():
    pag.press('space')
    pag.press('b')


def prestige():
    pag.press('p')


def invest():
    # open casino window
    # click casino tab
    # find invest button
    # click invest button
    # close casino
    return


def checkConvert():
    if ImageGrab.grab().getpixel((cards.convertLocation)) == (255, 255, 255):
        # if last convert was less than 5 seconds ago
        if convertTime is not None and time() - convertTime < 5:
            print('Full deck. Need to invest.')
            fullDeck = True
            # invest()
        else:
            convert()
        return True
    else:
        return False


def convert():
    pag.click(cards.convertLocation)
    sleep(0.5)
    confirm(cards.convertConfirmLocation)
    convertTime = time()


def confirm(confirmLocation):
    pag.click(confirmLocation)


def switchMode():
    if not ui.buyMaxMode:
        ui.buyMaxMode = True
        pag.click(ui.buyMaxLocation)
    else:
        ui.buyMaxMode = False
        pag.click(ui.buyOneLocation)


def checkFreeStuff():
    pag.click(cards.closeLocation)
    sleep(0.5)
    while ImageGrab.grab().getpixel((freestuff.activationLocation)) == (255, 255, 255):
        getFreeStuff()
        sleep(1)
    pag.click(cards.openLocation)


def getFreeStuff():
    pag.click(freestuff.activationLocation)
    sleep(0.5)
    confirm(freestuff.startLocation)
    sleep(6)
    confirm(freestuff.endLocation)

def buyLoop():
    time = 0
    while True:
        buyallAndRoll()
        time += 1
        sleep(1)

def prestigeLoop():
    time = 0
    while True:
        if time % freestuff.freeStuffInterVal == 0:
            checkFreeStuff()
        if time % 60 == 0:
            colors = ImageGrab.grab().crop((1567, 955, 1715, 980)).getcolors(maxcolors=512)
            for count, (r, g, b) in colors:
                if (r,g,b) == (103,135,58):
                    print('Prestige is green')   
                    sleep(ui.prestigeWaitTime)
                    prestige()
                    break
        buyallAndRoll()
        time += 1
        sleep(1)


def gameLoop():
    pag.click(ui.activateLocation)
    pag.click(cards.openLocation)
    sleep(1)
    time = 0
    prestigeTime = 0
    try:
        while not fullDeck:
            if time % freestuff.freeStuffInterVal == 0:
                checkFreeStuff()
            if time % 5 == 0:
                switchMode()
            buyallAndRoll()
            time += 1
            sleep(1)

    except KeyboardInterrupt:
        print('Program terminated')
        return 0


def setupUiConfigs():
    uiConfigs = UiConfigs()
    try:
        uiConfigs = pickle.load(file=open(f'uiConfigs_{screenWidth}x{screenHeight}.p', 'rb'))

    except FileNotFoundError:
        input('Move your mouse to the Activate area and press enter')
        uiConfigs.activateLocation = getMousePosition()
        input('Move your mouse to the Buy One button and press enter')
        uiConfigs.buyOneLocation = getMousePosition()
        input('Move your mouse to the Buy Max button and press enter')
        uiConfigs.buyMaxLocation = getMousePosition()

        pickle.dump(uiConfigs, file=open(f'uiConfigs_{screenWidth}x{screenHeight}.p', 'wb'))

    return uiConfigs


def setupfreestuffConfigs():
    freestuff = FreeStuffConfigs()
    try:
        freestuff = pickle.load(file=open(f'freestuff_{screenWidth}x{screenHeight}.p', 'rb'))

    except FileNotFoundError:
        input('Move your mouse to the Freestuff button and press enter')
        freestuff.activationLocation = getMousePosition()
        input('Move your mouse to the Start button and press enter')
        freestuff.startLocation = getMousePosition()
        input('Move your mouse to the End button and press enter')
        freestuff.endLocation = getMousePosition()

        pickle.dump(freestuff, file=open(f'freestuff_{screenWidth}x{screenHeight}.p', 'wb'))

    return freestuff


def setupCardsConfigs():
    cards = CardsConfigs()

    try:
        cards = pickle.load(file=open(f'cards_{screenWidth}x{screenHeight}.p', 'rb'))

    except FileNotFoundError:
        input('Move your mouse to the Cards button and press enter')
        cards.openLocation = getMousePosition()
        input('Move your mouse to the Convert button and press enter')
        cards.convertLocation = getMousePosition()
        input('Move your mouse to the Convert Confirm button and press enter')
        cards.convertConfirmLocation = getMousePosition()
        input('Move your mouse to the Close button and press enter')
        cards.closeLocation = getMousePosition()

        pickle.dump(cards, file=open(f'cards_{screenWidth}x{screenHeight}.p', 'wb'))

    return cards


def setup():
    ui = setupUiConfigs()
    freestuff = setupfreestuffConfigs()
    cards = setupCardsConfigs()
    return ui, freestuff, cards


def getMousePosition():
    return pag.position()


def main():
    pag.FAILSAFE = True
    # parse args
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--prestige', help='prestige only', required=False, default=False, action='store_true')
    parser.add_argument('-b', '--buy', help='buy only', required=False, default=False, action='store_true')
    arguments = parser.parse_args()
    
    #switch on arguments
    if(arguments.prestige):
        prestigeLoop()
    elif(arguments.buy):
        buyLoop()
    else:
        gameLoop()



    


if __name__ == '__main__':
    ui, freestuff, cards = setup()
    main()
