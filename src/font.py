import pygame
from src.constants import *
from src.image import Image
class Font:
    def __init__(self, size):
        self.font = pygame.font.SysFont(None, size)

    # Crée une Image avec le texte spécifié dessus.
    def render(self, text, antialias = False, color = BLACK, bgcolor = None):
        return Image(
            self.font.render(text, antialias, color, bgcolor)
        )