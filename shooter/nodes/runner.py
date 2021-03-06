from retro.src import retro
from shooter.path import asset
from shooter.nodes.enemy import Enemy

class Runner(Enemy):
    RUNNER_IMG = retro.Image(
        asset("bandit_street3.png"),
    )

    def __init__(self, stage):
        Enemy.__init__(self, self.RUNNER_IMG)
        self.stage = stage
        self.dx = -2

    def move(self):
        self.rect.x += self.dx
        if not self.stage.image.rect().contains(self.rect):
            self.dx *= -1
            self.image.flip(x = True, y = False)
            self.rect.clamp_ip(self.stage.image.rect())

    def update(self, target):
        Enemy.update(self, target)
        self.move()
