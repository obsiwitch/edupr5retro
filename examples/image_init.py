import os
import sys
import pygame
import numpy
from src.constants import *
from src.window import Window
from src.event import Event
from src.image import Image

PALETTE = {
    ' ': BLACK,
    'W': WHITE,
    'R': RED,
    'G': GREEN,
    'B': BLUE,
    'C': CYAN,
    'Y': YELLOW,
}

ASCII_IMG = (
    '                    ',
    '                    ',
    '          RRRR      ',
    '        RRYRRRR     ',
    '       RRYRR   R    ',
    '       RYYRRRR      ',
    '     RRRYYRYYRRR    ',
    '    RYRRYRYYYYRRR   ',
    '    RYYYYRRRYYYRR   ',
    '    RRYYRRRRYRRRR   ',
    '  R RRYRRRRRRYRR    ',
    '  R  RRYRRRRRYR     ',
    '  RRRRYYYRRRYYYR    ',
    '   RRRRYYYRYRRYR    ',
    '     RRRRRYYRRRR    ',
    '    R  RRYYRR RR    ',
    '     RRRRRRR  R     ',
    '       RRRR  R      ',
    '                    ',
    '                    ',
)

window = Window(
    title     = "window",
    size      = (640, 480),
    framerate = 30,
)
events = Event()

s1 = Image((100, 100))
s1_rect = s1.rect
s1_rect.move(10, 10)
print(s1.rect)
print(s1_rect)

s2 = Image.from_path(os.path.join(
    "examples", "data", "img.png"
))
s2_rect = s2.rect
s2_rect.move(10, 110)
s2_area = pygame.Rect(20, 10, 30, 30)

s3 = Image.from_ascii(ASCII_IMG, PALETTE)
s3_rect = s3.rect
s3_rect.move(10, 150)

s4 = s3.copy()
s4_rect = s3_rect.copy()
s4_rect.move(50, 0)

s5 = s4
s5_rect = s4_rect.copy()
s5_rect.move(50, 0)
s5.draw_line(GREEN, (0, 0), (30, 30))

while 1:
    events.update()
    if events.event(QUIT): sys.exit()

    window.fill(WHITE) \
          .draw_img(s1, s1_rect) \
          .draw_img(s2, s2_rect, s2_area) \
          .draw_img(s3, s3_rect) \
          .draw_img(s4, s4_rect) \
          .draw_img(s5, s5_rect)

    print(events.mouse_pos())

    window.update()
