from retro.src import retro
from pacman.game.entity import Entity
from pacman.game.assets import assets

class Powerup:
    def __init__(self):
        self.ticker = None

    @property
    def enabled(self):
        return self.ticker is not None and not self.ticker.finished

    @property
    def started(self):
        return self.enabled and (0 <= self.ticker.elapsed <= 1)

    def start(self):
        self.mul = 1
        self.ticker = retro.Ticker(end=300)

class Player(Entity):
    IMG = retro.Image(assets("pacman.png"))

    def __init__(self, pos):
        Entity.__init__(self,
            sprite = retro.Sprite(
                image = self.IMG,
                animations = retro.Animations(
                    frame_size = (32, 32),
                    period = 3,
                    STOP_L = ([2], 0), STOP_U = ([3], 0),
                    STOP_R = ([0], 0), STOP_D = ([4], 0),
                    WALK_L = ([2, 1], 0), WALK_U = ([3, 1], 0),
                    WALK_R = ([0, 1], 0), WALK_D = ([4, 1], 0),
                ),
            ),
            pos   = pos,
            speed = 4,
        )

        self.score = 0
        self.powerup = Powerup()

    @property
    def bounding_rect(self): return Entity.bounding_rect(self, 4)

    def collide_maze(self, maze):
        if self.curcol is None:
            if self.curdir[0]: self.rect.centerx = abs(
                self.rect.centerx - maze.rect.w
            )
            if self.curdir[1]: self.rect.centery = abs(
                self.rect.centery - maze.rect.h
            )
        elif not self.nxtcol:
            self.set_animation("WALK")
            self.curdir = self.nxtdir
        elif self.curcol:
            self.set_animation("STOP")
            return True
        return False

    def collide_bonus(self, maze):
        for i, j, b in maze.bonuses.neighborhood(self):
            if not b.rect.colliderect(self.bounding_rect): continue
            maze.bonuses.remove(i, j)
            if (b.id == b.BONUS2.id): self.powerup.start()
            self.score += b.value

    # Returns 0 if no collision happened,
    #         1 if the player killed a ghost,
    #        -1 if a ghost killed the player.
    def collide_ghost(self, ghosts):
        g = next((g for g in ghosts if g.bounding_rect.colliderect(
            self.bounding_rect
        )), None)
        if not g: return 0

        if g.state != g.state.FEAR: return -1

        g.kill()
        self.score += self.powerup.mul * g.BONUS
        self.powerup.mul *= 2
        return 1

    def update(self, maze):
        self.collide_bonus(maze)
        Entity.update(self, maze)

    def draw_score(self, image):
        font = retro.Font(36)
        txt = retro.Sprite(font.render(
            text    = f"SCORE: {self.score}",
            color   = retro.WHITE,
            bgcolor = retro.BLACK,
        ))
        txt.rect.bottomleft = image.rect().bottomleft
        txt.draw(image)
