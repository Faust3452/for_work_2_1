# pyautogui.doubleClick()     # Double click the mouse.
# >>> pyautogui.moveTo(500, 500, duration=2, tween=pyautogui.easeInOutQuad)  # Use tweening/easing function to move mouse over 2 seconds.
#
# >>> pyautogui.write('Hello world!', interval=0.25)  # type with quarter-second pause in between each key
# >>> pyautogui.press('esc')     # Press the Esc key. All key names are in pyautogui.KEY_NAMES
#
# >>> with pyautogui.hold('shift'):  # Press the Shift key down and hold it.
#         pyautogui.press(['left', 'left', 'left', 'left'])  # Press the left arrow key 4 times.
# >>> # Shift key is released automatically.
#pyautogui.FAILSAFE = False

#screenWidth, screenHeight = pyautogui.size()
#print(screenWidth, screenHeight) # 1920 x 1080

#positionMouseX, positionMouseY = pyautogui.position()
#print(positionMouseX, positionMouseY)
#pyautogui.moveTo(0, 0)
#pyautogui.moveTo(1895, 0)
#pyautogui.alert('This is the message to display.')
#print(pyautogui.KEY_NAMES)

import time, pyautogui, atexit

def cfg_import():
    curTime = get_time()
    try:
        with open('MoveChecker.cfg') as cfg:
            cfg = cfg.readlines()
            if len(cfg) == 1:
                cfg = cfg[0]
                cfg = cfg.replace('\r', '')
                cfg = cfg.replace('\n', '')
                if cfg.isdigit():
                    interval = int(cfg)
                    logger(5, curTime, interval)
                    return interval
                else:
                    raise Exception
            else:
                raise Exception
    except Exception:
        interval = 1
        logger(6, curTime)
        return interval

def get_time():
    return time.strftime('%d/%m/%Y %H:%M:%S timezone: %z')
def logger(event, curTime, interval=1):
    if event == 0:
        event = 'Program Started!!!'
    if event == 1:
        event = 'Nothing Changed, message appeared'
    if event == 2:
        event = 'Position Changed'
    if event == 3:
        event = 'Reaction at the box message'
    if event == 4:
        event = 'Program Closed\n'
    if event == 5:
        event = f'Interval parameter is good, interval is {interval} minute(s)'
    if event == 6:
        event = f'Something wrong with cfg file or there is no one, interval is {interval} minute(s)'
    with open('MoveChecker.log', mode='a+') as log:
        log.write(f'{curTime}: {event}\n')

pyautogui.FAILSAFE = False
screenWidth, screenHeight = pyautogui.size()
currentPositionMouseX, currentPositionMouseY = pyautogui.position()
positionMouseX, positionMouseY = 0, 0
currentTime = get_time()
print(f'Start time: {currentTime}')
logger(0, currentTime)
sleepingInterval = cfg_import() * 60
print(sleepingInterval)
try:
    while True:
        currentTime = get_time()
        currentPositionMouseX, currentPositionMouseY = pyautogui.position()
        if currentPositionMouseX == positionMouseX and currentPositionMouseY == positionMouseY:
            event = f'{currentTime}: Nothing changed'
            print(event)
            logger(1, currentTime)
            pyautogui.alert('You doing nothing, filthy shit!', button='I understood')
            currentTime = get_time()
            logger(3, currentTime)
        else:
            event = f'{currentTime}: Position changed'
            print(event)
            logger(2, currentTime)
            positionMouseX = currentPositionMouseX
            positionMouseY = currentPositionMouseY
        time.sleep(sleepingInterval)
except KeyboardInterrupt:
    currentTime = get_time()
    logger(4, currentTime)

except Exception as e:
    currentTime = get_time()
    logger(e, currentTime)

atexit.register(logger, event='Program closed', currentTime=get_time())