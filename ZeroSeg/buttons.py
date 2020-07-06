#!/usr/bin/env python3

from RPi import GPIO
from typing import Literal


class Button:
    def __init__(self):
        self.switch1 = 17
        self.switch2 = 26
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.switch1, GPIO.IN)
        GPIO.setup(self.switch2, GPIO.IN)

    def pressed(self, button: Literal["left", "right"]) -> bool:
        """
        Get button status (bool), check if is pressed.
        """
        if button == "left":
            if not GPIO.input(self.switch1):
                return True
            else:
                return False
        elif button == "right":
            if not GPIO.input(self.switch2):
                return True
            else:
                return False
        else:
            raise ValueError("Invalid button name, allowed: 'left', 'right'.")
