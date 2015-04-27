class InputManager:
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