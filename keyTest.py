from pynput.keyboard import Key, Controller
keyboard = Controller()

keyboard.press(Key.cmd)
keyboard.press(Key.ctrl)
keyboard.press('o')
keyboard.release('o')
keyboard.release(Key.ctrl)
keyboard.release(Key.cmd)

#keyboard.press('o')
#keyboard.release('o')

#keyboard.press('s')
#keyboard.release('s')

#keyboard.press('k')
#keyboard.release('k')



#keyboard.press(Key.enter)
#keyboard.release(Key.enter)