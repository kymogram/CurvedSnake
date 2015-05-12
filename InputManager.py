class InputManager:
    '''
        InputManager class is used to store the pressed keys
        to know when snakes must change direction
    '''

    def __init__(self):
        self.pressed_keys = dict()

    def press(self, key):
        self.pressed_keys[key] = True

    def release(self, key):
        self.pressed_keys[key] = False

    def isPressed(self, key):
        try:
            return self.pressed_keys[key]
        except:
            return False
