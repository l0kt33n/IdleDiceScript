from PIL import ImageGrab
from time import sleep
import pyautogui as pag
import pickle


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


def buyallAndRoll():
    pag.press('space')
    pag.press('b')


def prestige():
    pag.press('p')


def checkConvert(cards: CardsConfigs):
    if ImageGrab.grab().getpixel((cards.convertLocation)) == (255, 255, 255):
        convert(cards)
        return True
    else:
        return False


def convert(cards: CardsConfigs):
    pag.click(cards.convertLocation)
    sleep(0.5)
    confirm(cards.convertConfirmLocation)


def confirm(confirmLocation):
    pag.click(confirmLocation)


def switchMode(options: UiConfigs):
    if not options.buyMaxMode:
        options.buyMaxMode = True
        pag.click(options.buyMaxLocation)
    else:
        options.buyMaxMode = False
        pag.click(options.buyOneLocation)


def checkFreeStuff(cards: CardsConfigs, freestuff: FreeStuffConfigs):
    pag.click(cards.closeLocation)
    sleep(0.5)
    while ImageGrab.grab().getpixel((freestuff.activationLocation)) == (255, 255, 255):
        getFreeStuff(freestuff)
        sleep(1)
    pag.click(cards.openLocation)


def getFreeStuff(freestuff: FreeStuffConfigs):
    pag.click(freestuff.activationLocation)
    sleep(0.5)
    confirm(freestuff.startLocation)
    sleep(6)
    confirm(freestuff.endLocation)


def gameLoop(ui: UiConfigs, cards: CardsConfigs, freestuff: FreeStuffConfigs):
    pag.click(ui.activateLocation)
    pag.click(cards.openLocation)
    sleep(1)
    time = 0
    prestigeTime = 0
    try:
        while True:
            if time % freestuff.freeStuffInterVal == 0:
                checkFreeStuff(cards, freestuff)
            if checkConvert(cards):
                prestigeTime = 0
            else:
                prestigeTime += 1
                if prestigeTime >= ui.prestigeWaitTime:
                    prestige()
                    prestigeTime = 0
                if prestigeTime % 5 == 0:
                    switchMode(ui)
            buyallAndRoll()
            time += 1
            sleep(1)
    except KeyboardInterrupt:
        print('Program terminated')
        return 0


def setupUiConfigs():
    uiConfigs = UiConfigs()
    try:
        uiConfigs = pickle.load(file=open('uiConfigs.p', 'rb'))

    except FileNotFoundError:
        input('Move your mouse to the Activate area and press enter')
        uiConfigs.activateLocation = getMousePosition()
        input('Move your mouse to the Buy One button and press enter')
        uiConfigs.buyOneLocation = getMousePosition()
        input('Move your mouse to the Buy Max button and press enter')
        uiConfigs.buyMaxLocation = getMousePosition()

        pickle.dump(uiConfigs, file=open('uiConfigs.p', 'wb'))
        
    return uiConfigs


def setupFreestuffsConfigs():
    freestuffs = FreeStuffConfigs()
    try:
        freestuffs = pickle.load(file=open('freestuffs.p', 'rb'))
        
    except FileNotFoundError:
        input('Move your mouse to the Freestuff button and press enter')
        freestuffs.activationLocation = getMousePosition()
        input('Move your mouse to the Start button and press enter')
        freestuffs.startLocation = getMousePosition()
        input('Move your mouse to the End button and press enter')
        freestuffs.endLocation = getMousePosition()

        pickle.dump(freestuffs, file=open('freestuffs.p', 'wb'))
    
    return freestuffs


def setupCardsConfigs():
    cards = CardsConfigs()
    
    try:
        cards = pickle.load(file=open('cards.p', 'rb'))
        
    except FileNotFoundError:
        input('Move your mouse to the Cards button and press enter')
        cards.openLocation = getMousePosition()
        input('Move your mouse to the Convert button and press enter')
        cards.convertLocation = getMousePosition()
        input('Move your mouse to the Convert Confirm button and press enter')
        cards.convertConfirmLocation = getMousePosition()
        input('Move your mouse to the Close button and press enter')
        cards.closeLocation = getMousePosition()

        pickle.dump(cards, file=open('cards.p', 'wb'))

    return cards

def setup():
    ui = setupUiConfigs()
    freestuffs = setupFreestuffsConfigs()
    cards = setupCardsConfigs()
    return ui, freestuffs, cards

def getMousePosition():
    return pag.position()


def main():
    pag.FAILSAFE = True
    ui, freestuffs, cards = setup()
    gameLoop(ui, cards, freestuffs)


if __name__ == '__main__':
    main()
