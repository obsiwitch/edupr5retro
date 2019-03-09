import os
from src.constants import *
from src.window import Window
from src.image import Image

window = Window(
    title     = "window",
    size      = (640, 480),
    framerate = 30,
)

spritesheet = Image.from_path(os.path.join(
    "tests", "data", "spritesheet.png"
))
spritesheet[0, 0] = GREEN
assert spritesheet[0, 0] == GREEN

background = Image(window.rect().size) \
           .fill(WHITE) \
           .draw_img(spritesheet, (0, 0))

def main():
    pos = window.events.mouse_pos()
    if window.events.mouse_hold(): background[pos] = GREEN
    print(background[pos])

    window.draw_img(background, (0, 0))

window.loop(main)
