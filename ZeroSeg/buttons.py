#!/usr/bin/env python3

from RPi import GPIO


class Button:
    def __init__(self, button: str):
        """
        Accepted values: 'left', 'right'.
        """
        if button == "left":
            self.button = 17
        elif button == "right":
            self.button = 26
        else:
            raise ValueError("Invalid button name, allowed: 'left', 'right'.")
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.button, GPIO.IN)

    def pressed(self) -> bool:
        """
        Get button status (bool), check if is pressed.
        """
        if not GPIO.input(self.button):
            return True
        else:
            return False
