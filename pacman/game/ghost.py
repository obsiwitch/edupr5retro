import random
import numpy
from retro.src import retro
from pacman.game.entity import Entity
from pacman.game.assets import assets

class Ghosts(retro.Group):
    def __init__(self, max, pos):
        retro.Group.__init__(self, Ghost(pos))
        self.max = max
        self.pos = pos
        self.spawn_ticker = retro.Ticker(end=300)

    def notify_kill(self):
        # countermeasure to avoid instant repop
        if len(self) == self.max:
            self.spawn_ticker.restart()

    def update(self, maze, player):
        retro.Group.update(self, maze, player)

        if len(self) == self.max: return
        elif self.spawn_ticker.finished:
            self.append(Ghost(self.pos))
            self.spawn_ticker.restart()

class State:
    WALK = 0
    FEAR = 1

    def __init__(self, ghost):
        self.ghost = ghost
        self.current = self.WALK

    def __eq__(self, v): return (self.current == v)

    def update(self, player):
        if self.current == self.WALK:
            if player.powerup.started:
                self.ghost.set_animation("FEAR")
                self.ghost.curdir = numpy.negative(self.ghost.curdir).tolist()
                self.current = self.FEAR
        elif self.current == self.FEAR:
            if not player.powerup.enabled:
                self.ghost.set_animation("WALK")
                self.current = self.WALK

class Ghost(Entity):
    IMG = retro.Image(assets("ghost.png"))
    BONUS = 200

    def __init__(self, pos):
        Entity.__init__(self,
            sprite = retro.Sprite(
                image = self.IMG,
                animations = retro.Animations(
                    frame_size = (32, 32),
                    period = 3,
                    WALK_L = ([0], 0), WALK_U = ([0], 0),
                    WALK_R = ([0], 0), WALK_D = ([0], 0),
                    FEAR_L = ([1], 0), FEAR_U = ([1], 0),
                    FEAR_R = ([1], 0), FEAR_D = ([1], 0),
                ),
            ),
            pos   = pos,
            speed = 2,
            curdir = [0, 0],
            nxtdir = random.choice(([-1, 0], [1, 0])),
        )

        self.state = State(self)

    @property
    def bounding_rect(self): return Entity.bounding_rect(self, 12)

    def next_dir(self):
        dirs = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        opdir = numpy.negative(self.curdir).tolist()
        if opdir in dirs: dirs.remove(opdir)
        self.nxtdir = random.choice(dirs)

    def collide_maze(self, maze):
        if not self.nxtcol:
            self.curdir = self.nxtdir
        elif self.curcol is None:
            self.curdir = numpy.negative(self.curdir).tolist()

        elif self.curcol:
            self.next_dir()
            return True

        return False

    def kill(self):
        for g in self.groups: g.notify_kill()
        Entity.kill(self)

    def update(self, maze, player):
        self.state.update(player)
        if (self.curdir == self.nxtdir):
            self.next_dir()
        Entity.update(self, maze)
