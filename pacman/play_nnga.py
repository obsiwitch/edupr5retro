import itertools
import types
import time
import sys
import numpy
import pygame
from retro.src import retro
from pacman.game.game import Game, Games
from pacman.game.maze import Maze
from pacman.nnga import NNGAPool

class PlayNNGA:
    def __init__(self):
        self.nn_pool = NNGAPool(size = 200, arch = (10, 10, 10, 4))
        self.window = retro.Window(title='Pacman', size=(448, 528), fps=-1)
        self.games = Games(size = len(self.nn_pool))

    def update_one(self, game, nn):
        if game.finished: return False

        maze   = game.maze
        player = game.player
        ghost  = game.target(game.ghosts)
        bonus  = maze.bonuses.nearest(player)

        p = nn.predict(
            *numpy.subtract(
                ghost.rect.center, player.rect.center
            ) if ghost else (-1.0, -1.0),
            ghost.state.current if ghost else -1,
            *numpy.subtract(
                bonus.rect.center, player.rect.center
            ) if bonus else (-1.0, -1.0),
            maze.bonuses.count,
            *maze.walls.floor_cells(
                *maze.tile_pos(player.rect.center)
            )
        )

        dirs = ([-1, 0], [ 0, -1], [ 1,  0], [ 0,  1])
        i = sorted(
            range(len(p)),
            key = lambda i: p[i],
            reverse = True,
        )[0]
        player.nxtdir = dirs[i]

        game.update()

    def update_many(self):
        for i, game in enumerate(self.games):
            self.update_one(game, self.nn_pool[i])

    def render(self):
        self.games.best.render(self.window)

    def main(self):
        while self.nn_pool.generation <= 50:
            # Update
            start = time.time()
            while not self.games.finished:
                self.window.step(self.update_many, self.render)
            end = time.time()

            # Evolve
            best = self.nn_pool.evolve(self.games)
            print(self.nn_pool.generation - 1, best.fitness, end - start)
            self.games.reset()

PlayNNGA().main()
