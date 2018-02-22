import pygame

from shared.math  import Directions
from shared.collisions import *
from maze.palette import palette
from maze.maze    import Maze
from maze.player  import Player

class StateRun:
    def __init__(self, window):
        self.window = window

        self.player = Player(window)
        self.maze = Maze(window)

        self.win = False

    def draw_score(self):
        score_surface = self.window.fonts[0].render(
            f"Score: {self.player.score}", # text
            False,                         # antialias
            pygame.Color("white")          # color
        )
        self.window.screen.blit(
            score_surface,
            score_surface.get_rect(
                topright = self.window.rect.topright
            ).move(-10, 10)
        )

    def run(self):
        # Update
        self.player.update(
            directions = Directions(
                up    = self.window.keys[pygame.K_UP],
                down  = self.window.keys[pygame.K_DOWN],
                left  = self.window.keys[pygame.K_LEFT],
                right = self.window.keys[pygame.K_RIGHT],
            ),
            collisions = pixel_collision_vertices(
                surface = self.window.screen,
                rect    = self.player.sprite.rect,
                color   = pygame.Color(*palette["B"]),
            ),
        )

        ## Traps
        if pygame.sprite.spritecollide(
            self.player.sprite, # sprite
            self.maze.traps,    # group
            False               # dokill
        ): self.player.reset_position()

        ## Treasures
        if pygame.sprite.spritecollide(
            self.player.sprite,  # sprite
            self.maze.treasures, # group
            True                 # dokill
        ): self.player.score += 100

        ## Exit
        self.win = distance_collision(
            p1 = self.player.sprite.rect.center,
            p2 = self.maze.exit.rect.center,
            threshold = 5
        )

        # Draw
        self.maze.draw()
        self.player.draw()
        self.draw_score()

        return False
