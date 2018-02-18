import sys
import pygame

class Window:
    @property
    def width(self): return self.rect.width
    @property
    def height(self): return self.rect.height

    def __init__(self, width, height, title, cursor = False):
        pygame.init()

        self.screen = pygame.display.set_mode([width, height])
        self.rect = self.screen.get_rect()

        pygame.display.set_caption(title)
        pygame.mouse.set_visible(cursor)

        self.clock = pygame.time.Clock()

        self.events = []

    def loop(self, instructions):
        while 1:
            self.events = pygame.event.get()
            for event in self.events:
                if event.type == pygame.QUIT: sys.exit()

            self.keys = pygame.key.get_pressed()

            instructions()

            self.clock.tick(30) # 30 FPS

            pygame.display.flip() # update display Surface
