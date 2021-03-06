import numpy
from retro.src import retro
from pacman.game.maze import Walls

class Entity(retro.Sprite):
    def __init__(self, sprite, pos, speed, curdir = [0, 0], nxtdir = [0, 0]):
        retro.Sprite.__init__(self, sprite.image, sprite.animations)
        self.rect.topleft = pos
        self.speed  = speed
        self.curdir = curdir
        self.nxtdir = nxtdir

    def set_animation(self, name):
        if   self.curdir[0] == -1: self.animations.set(f"{name}_L")
        elif self.curdir[0] ==  1: self.animations.set(f"{name}_R")
        elif self.curdir[1] == -1: self.animations.set(f"{name}_U")
        elif self.curdir[1] ==  1: self.animations.set(f"{name}_D")

    def bounding_rect(self, offset):
        r = self.rect.copy()
        r.size = numpy.subtract(r.size, offset).tolist()
        r.center = self.rect.center
        return r

    @property
    def curcol(self):
        return Walls.px3(self.curdir, self.rect)

    @property
    def nxtcol(self):
        return Walls.px3(self.nxtdir, self.rect)

    def collide_maze(self, maze):
        raise NotImplementedError

    def update(self, maze):
        if not self.collide_maze(maze):
            self.rect.move_ip(numpy.multiply(self.speed, self.curdir))
