import keyboard
from pathlib import Path
from core import ScreenBacklight

from rich.progress import Progress, BarColumn

screen = ScreenBacklight(Path("/sys/class/backlight/intel_backlight"))

total = screen.get_max_brightness()

def adjust_brightness(progress: Progress, task, sep):
    screen.adjust_brightness(+sep)
    progress.advance(task, +sep)
    progress.refresh()
    
def brightness_plus(progress: Progress, task, sep):
    try:
        adjust_brightness(progress, task, +sep)
    except OSError:
        screen.set_brightness(total)
        progress.reset(task, completed=total)
        progress.refresh()

def brightness_reduce(progress: Progress, task, sep):
    try:
        adjust_brightness(progress, task, -sep)
    except OSError:
        screen.set_brightness(0)
        progress.reset(task, completed=0)
        progress.refresh()

with Progress("{task.description}",
              BarColumn(),
              "{task.percentage:>3.0f}%",
              auto_refresh=False) as progress:
    task = progress.add_task("Light",
                             total=total,
                             completed=screen.get_brightness())
    keyboard.add_hotkey("up",
                        brightness_plus,
                        args=(progress, task, total // 100))
    keyboard.add_hotkey("right",
                        brightness_plus,
                        args=(progress, task, total // 100 * 5))
    keyboard.add_hotkey("down",
                        brightness_reduce,
                        args=(progress, task, total // 100))
    keyboard.add_hotkey("left",
                        brightness_reduce,
                        args=(progress, task, total // 100 * 5))
    keyboard.wait("esc")
