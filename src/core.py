#!/usr/bin/env python3
from pathlib import Path

class ScreenBacklight:
    def __init__(self, device_path: Path):
        self._brightness = device_path/"brightness"
        self._max_brightness = self.read_int(device_path/"max_brightness")

    @staticmethod
    def read_int(file: Path) -> int:
        return int(file.read_text())

    @staticmethod
    def write_int(file: Path, number: int) -> None:
        file.write_text(str(number))

    def get_brightness(self) -> int:
        return self.read_int(self._brightness)

    def get_max_brightness(self) -> int:
        return self._max_brightness

    def set_brightness(self, brightness: int) -> None:
        self.write_int(self._brightness, brightness)

    def adjust_brightness(self, value: int) -> None:
        self.set_brightness(self.get_brightness() + value)

