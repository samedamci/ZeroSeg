#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from typing import Union, List


class constants(object):
    MAX7219_REG_NOOP = 0x0
    MAX7219_REG_DIGIT0 = 0x1
    MAX7219_REG_DIGIT1 = 0x2
    MAX7219_REG_DIGIT2 = 0x3
    MAX7219_REG_DIGIT3 = 0x4
    MAX7219_REG_DIGIT4 = 0x5
    MAX7219_REG_DIGIT5 = 0x6
    MAX7219_REG_DIGIT6 = 0x7
    MAX7219_REG_DIGIT7 = 0x8
    MAX7219_REG_DECODEMODE = 0x9
    MAX7219_REG_INTENSITY = 0xA
    MAX7219_REG_SCANLIMIT = 0xB
    MAX7219_REG_SHUTDOWN = 0xC
    MAX7219_REG_DISPLAYTEST = 0xF


class device(object):
    """
    Base class for handling multiple cascaded MAX7219 devices.
    Callers should generally pick the `sevensegment` class

    A buffer is maintained which holds the bytes that will be cascaded
    every time `flush` is called.
    """

    NUM_DIGITS = 8

    def __init__(self, spi_bus: int = 0, spi_device: int = 0, vertical: bool = False):
        """
        Constructor: `vertical` should be set to True if the text should start from
        the header instead perpendicularly.
        """
        import spidev

        self._buffer = [0] * self.NUM_DIGITS * 2
        self._spi = spidev.SpiDev()
        self._spi.open(spi_bus, spi_device)
        self._vertical = vertical

        self.command(constants.MAX7219_REG_SCANLIMIT, 7)  # show all 8 digits
        self.command(constants.MAX7219_REG_DECODEMODE, 0)  # use matrix (not digits)
        self.command(constants.MAX7219_REG_DISPLAYTEST, 0)  # no display test
        self.command(constants.MAX7219_REG_SHUTDOWN, 1)  # not shutdown mode
        self.brightness(7)  # intensity: range: 0..15
        self.clear()

    def command(self, register: int, data: int):
        """
        Sends a specific register and some data.
        """
        assert (
            constants.MAX7219_REG_DECODEMODE
            <= register
            <= constants.MAX7219_REG_DISPLAYTEST
        )
        self._write([register, data])

    def _write(self, data: list):
        """
        Send the bytes (which should comprise of alternating command,
        data values) over the SPI device.
        """
        self._spi.xfer(list(data), 5000000)

    def _values(self, position: int, buf: List[int]) -> Union[int, List[int]]:
        """
        A generator which yields the digit/column position and the data
        value from that position.
        """
        yield position + constants.MAX7219_REG_DIGIT0
        yield buf[self.NUM_DIGITS + position]

    def clear(self):
        """
        Clears the buffer of the device.
        """
        for position in range(self.NUM_DIGITS):
            self.set_byte(0, position + constants.MAX7219_REG_DIGIT0, redraw=False)

        self.flush()

    def _preprocess_buffer(self, buf):
        """
        Overload in subclass to provide custom behaviour: see
        matrix implementation for example. Returns argument.
        """
        return buf

    def flush(self):
        """
        For each digit/column, cascade out the contents of the buffer
        cells to the SPI device.
        """
        # Allow subclasses to pre-process the buffer: they shouldn't
        # alter it, so make a copy first.
        buf = self._preprocess_buffer(list(self._buffer))
        assert len(buf) == len(self._buffer), "Preprocessed buffer is wrong size."
        if self._vertical:
            tmp_buf = []
            tmp_buf += buf[8 + 8 : 8]
            buf = tmp_buf

        for posn in range(self.NUM_DIGITS):
            self._write(self._values(posn, buf))

    def brightness(self, intensity: int):
        """
        Sets the brightness level of screen ranging from 0..15. Note that setting
        the brightness to a high level will draw more current, and may cause
        intermittent issues / crashes if the USB power source is insufficient.
        """
        assert 0 <= intensity < 16, "Invalid brightness: {intensity}."
        self.command(constants.MAX7219_REG_INTENSITY, intensity)

    def set_byte(self, value: int, position: int, redraw: bool = True):
        """
        Low level mechanism to set a byte value in the buffer array. If redraw
        is not suppled, or set to True, will force a redraw of all buffer
        items. If you are calling this method rapidly/frequently (e.g in a
        loop), it would be more efficient to set to False, and when done,
        call `flush`.

        Prefer to use the higher-level method calls in the subclasses below.
        """
        assert (
            constants.MAX7219_REG_DIGIT0 <= position <= constants.MAX7219_REG_DIGIT7
        ), f"Invalid digit/column: {position}"
        assert 0 <= value < 256, f"Value {value} outside range 0..255."

        offset = self.NUM_DIGITS + position - constants.MAX7219_REG_DIGIT0
        self._buffer[offset] = value

        if redraw:
            self.flush()

    def rotate_left(self, redraw: bool = True):
        """
        Scrolls the buffer one column to the left. The data that scrolls off
        the left side re-appears at the right-most position. If redraw
        is not suppled, or left set to True, will force a redraw of all buffer
        items.
        """
        t = self._buffer[-1]
        for i in range(self.NUM_DIGITS - 1, 0, -1):
            self._buffer[i] = self._buffer[i - 1]
        self._buffer[0] = t
        if redraw:
            self.flush()

    def rotate_right(self, redraw: bool = True):
        """
        Scrolls the buffer one column to the right. The data that scrolls off
        the right side re-appears at the left-most position. If redraw
        is not suppled, or left set to True, will force a redraw of all buffer
        items.
        """
        t = self._buffer[0]
        for i in range(0, self.NUM_DIGITS - 1, 1):
            self._buffer[i] = self._buffer[i + 1]
        self._buffer[-1] = t
        if redraw:
            self.flush()

    def scroll_left(self, redraw: bool = True):
        """
        Scrolls the buffer one column to the left. Any data that scrolls off
        the left side is lost and does not re-appear on the right. An empty
        column is inserted at the right-most position. If redraw
        is not suppled, or set to True, will force a redraw of all buffer
        items.
        """
        del self._buffer[0]
        self._buffer.append(0)
        if redraw:
            self.flush()

    def scroll_right(self, redraw: bool = True):
        """
        Scrolls the buffer one column to the right. Any data that scrolls off
        the right side is lost and does not re-appear on the left. An empty
        column is inserted at the left-most position. If redraw
        is not suppled, or set to True, will force a redraw of all buffer
        items.
        """
        del self._buffer[-1]
        self._buffer.insert(0, 0)
        if redraw:
            self.flush()


class sevensegment(device):
    """
    Implementation of MAX7219 devices cascaded with a series of seven-segment
    LEDs. It provides a convenient method to write a number to a given device
    in octal, decimal or hex, flushed left/right with zero padding. Base 10
    numbers can be either integers or floating point (with the number of
    decimal points configurable).
    """

    _UNDEFINED = 0x08
    _RADIX = {8: "o", 10: "f", 16: "x"}
    # Some letters cannot be represented by 7 segments, so dictionary lookup
    # will default to _UNDEFINED (an underscore) instead.
    _DIGITS = {
        " ": 0x00,
        "-": 0x01,
        "_": 0x08,
        "0": 0x7E,
        "1": 0x30,
        "2": 0x6D,
        "3": 0x79,
        "4": 0x33,
        "5": 0x5B,
        "6": 0x5F,
        "7": 0x70,
        "8": 0x7F,
        "9": 0x7B,
        "a": 0x7D,
        "b": 0x1F,
        "c": 0x0D,
        "d": 0x3D,
        "e": 0x6F,
        "f": 0x47,
        "g": 0x7B,
        "h": 0x17,
        "i": 0x10,
        "j": 0x18,
        # 'k': cant represent
        "l": 0x06,
        # 'm': cant represent
        "n": 0x15,
        "o": 0x1D,
        "p": 0x67,
        "q": 0x73,
        "r": 0x05,
        "s": 0x5B,
        "t": 0x0F,
        "u": 0x1C,
        "v": 0x1C,
        # 'w': cant represent
        # 'x': cant represent
        "y": 0x3B,
        "z": 0x6D,
        "A": 0x77,
        "B": 0x7F,
        "C": 0x4E,
        "D": 0x7E,
        "E": 0x4F,
        "F": 0x47,
        "G": 0x5E,
        "H": 0x37,
        "I": 0x30,
        "J": 0x38,
        # 'K': cant represent
        "L": 0x0E,
        # 'M': cant represent
        "N": 0x76,
        "O": 0x7E,
        "P": 0x67,
        "Q": 0x73,
        "R": 0x46,
        "S": 0x5B,
        "T": 0x0F,
        "U": 0x3E,
        "V": 0x3E,
        # 'W': cant represent
        # 'X': cant represent
        "Y": 0x3B,
        "Z": 0x6D,
        ",": 0x80,
        ".": 0x80,
    }

    def write_char(
        self,
        char: str = None,
        position: int = 1,
        dot: bool = False,
        redraw: bool = True,
    ):
        """
        Looks up the most appropriate character representation for char
        from the digits table, and writes that bitmap value into the buffer
        at the given position.
        """
        assert dot in [0, 1, False, True]
        value = self._DIGITS.get(str(char), self._UNDEFINED) | (dot << 7)
        self.set_byte(value, position, redraw)

    def write_number(
        self,
        value: float,
        base: int = 10,
        decimal_places: int = 0,
        zero_pad: bool = False,
        left_justify: bool = False,
    ):
        """
        Formats the value according to the parameters supplied, If the formatted
        number is larger than 8 digits, then an OverflowError is raised.
        """
        assert base in self._RADIX, f"Invalid base: {base}"

        # Magic up a printf format string
        size = self.NUM_DIGITS
        format_str = "%"

        if zero_pad:
            format_str += "0"

        if decimal_places > 0:
            size += 1

        if left_justify:
            size *= -1

        format_str = f"{format_str}{size}.{decimal_places}{self._RADIX[base]}"

        position = constants.MAX7219_REG_DIGIT7
        str_value = format_str % value

        # Go through each digit in the formatted string,
        # updating the buffer accordingly
        for char in str_value:

            if position < constants.MAX7219_REG_DIGIT0:
                self.clear()
                raise OverflowError(f"{str_value} too large for display")

            if char == ".":
                continue

            dp = decimal_places > 0 and position == decimal_places + 1
            self.write_char(char, position, dot=dp, redraw=False)
            position -= 1

        self.flush()

    def write_text(self, text: str):
        """
        Outputs the text as near as possible. If text is larger than 8 characters,
        then an OverflowError is raised.
        """
        if len(text) > 8:
            raise OverflowError(f"{text} too large for display")
        for pos, char in enumerate(text.ljust(8)[::-1]):
            self.write_char(char, constants.MAX7219_REG_DIGIT0 + pos, redraw=False)

        self.flush()

    def show_message(self, text: str, delay: float = 0.4):
        """
        Transitions the text message from left-to-right.
        """
        # Add some spaces on so that the message scrolls off to the left completely.
        text += " " * self.NUM_DIGITS * 2
        for value in text:
            time.sleep(delay)
            self.scroll_right(redraw=False)
            self._buffer[0] = self._DIGITS.get(value, self._UNDEFINED)
            self.flush()
