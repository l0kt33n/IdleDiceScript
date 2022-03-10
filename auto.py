import pyscreenshot as ImageGrab
from time import sleep, time
import pyautogui as pag
import pickle
import argparse

convertTime = None
fullDeck = False
prestigeCountdown = 0
screenWidth, screenHeight = pag.size()


class UiConfigs():
    def __init__(self):
        self.activateLocation = (841, 420)
        self.buyOneLocation = (1602, 66)
        self.buyMaxLocation = (1869, 66)
        self.buyMaxMode = False
        self.prestigeWaitTime = 120
        self.presL1Location = (1250, 671)
        self.presL2Location = (1250, 671)


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
    while ImageGrab.grab().getpixel((freestuff.activationLocation)) == (255, 255, 255):
        getFreeStuff()
        sleep(1)


def getFreeStuff():
    pag.click(freestuff.activationLocation)
    sleep(1)
    confirm(freestuff.startLocation)
    sleep(1)
    confirm(freestuff.endLocation)


def buyLoop():
    time = 0
    while True:
        buyallAndRoll()
        time += 1
        sleep(1)


def prestigeLoop():
    time = 0
    prestigeCountdown = -1
    lastPrestigeTime = -1
    prestigeWaitTime = 600
    while True:
        if time % 60 == 0:
            getFreeStuff()
        if time % 5 == 0:
            switchMode()
        if prestigeCountdown == 0:
            prestige()
            lastPrestigeTime = time
            prestigeCountdown = -1
        if time - lastPrestigeTime > prestigeWaitTime and prestigeCountdown <= 0:
            prestige()
            lastPrestigeTime = time
            prestigeCountdown = -1
            prestigeWaitTime += 30
        if time % 10 == 0 and prestigeCountdown <= 0 and time-lastPrestigeTime > 5:
            colors = ImageGrab.grab().crop(
                (ui.presL1Location[0], ui.presL1Location[1], ui.presL2Location[0], ui.presL1Location[1])).getcolors(maxcolors=1024)
            for count, (r, g, b) in colors:
                if g > r and g > b:
                    prestigeCountdown = ui.prestigeWaitTime
                    break
        if prestigeCountdown > 0:
            prestigeCountdown -= 1
            print(prestigeCountdown)
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
                getFreeStuff()
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
        input('Move your mouse to the Prestige button top left and press enter')
        uiConfigs.presL1Location = getMousePosition()
        input('Move your mouse to the Prestige button bottom right and press enter')
        uiConfigs.presL2Location = getMousePosition()

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
    parser.add_argument('-p', '--prestige', help='prestige only',
                        required=False, default=False, action='store_true')
    parser.add_argument('-b', '--buy', help='buy only',
                        required=False, default=False, action='store_true')
    arguments = parser.parse_args()

    # switch on arguments
    if(arguments.prestige):
        prestigeLoop()
    elif(arguments.buy):
        buyLoop()
    else:
        gameLoop()


if __name__ == '__main__':
    ui, freestuff, cards = setup()
    main()
