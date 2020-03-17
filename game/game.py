import types
import retro
from game.maze import Maze
from game.player import Player
from game.ghost import Ghost, Ghosts

class Games(list):
    def __init__(self, window, parameters, size):
        list.__init__(self, [Game(window, parameters) for _ in range(size)])

    @property
    def finished(self): return all(g.finished for g in self)

    @property
    def best(self): return sorted(
        self,
        key = lambda g: g.fitness,
        reverse = True
    )[0]

    def reset(self):
        for g in self: g.reset()

class Game:
    def __init__(self, window, parameters):
        self.window   = window
        self.parameters = parameters
        self.maze     = Maze(parameters.name)
        self.player   = Player(parameters.player_pos)
        self.ghosts   = Ghosts(parameters.ghosts_num, parameters.ghosts_pos)
        self.finished = False

    @property
    def fitness(self): return self.player.score

    def target(self, iterable):
        target = sorted(
            iterable,
            key = lambda elem: Maze.distance(
                self.player.rect.center,
                elem.rect.center
            )
        )
        if target: return target[0]

    def update(self):
        self.player.update(self.maze)
        self.ghosts.update(self.maze, self.player)

        self.finished = (self.maze.bonuses.count <= 0) \
                     or (self.player.collide_ghost(self.ghosts) == -1)

    def draw(self):
        self.window.fill(retro.BLACK)
        self.maze.draw(self.window)
        self.ghosts.draw(self.window)
        self.player.draw(self.window)
        self.player.draw_score(self.window)

    def reset(self): self.__init__(self.window, self.parameters)
