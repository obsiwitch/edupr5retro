import shared.collisions
from shared.background import Background
from shared.sprite import Sprite
from lemmings.nodes.spawner import Spawner
from lemmings.path import asset_path
from lemmings.ui import UI

class Level:
    def __init__(self, window, map, startp, endp):
        self.window = window
        self.bg = Background(asset_path(map))

        self.ui = UI(self.window)

        self.spawner = Spawner(self.window, self.bg, startp)
        self.exit = Sprite.from_path(asset_path("sortie.png"))
        self.exit.rect.topleft = endp

    @property
    def win(self): return (self.spawner.escaped >= 10)

    @property
    def lost(self): return (
        self.spawner.generated and (len(self.spawner.group) <= 0)
    )

    def run(self):
        # update
        self.ui.update()
        self.spawner.update(self.ui.selection.state)

        if shared.collisions.sprites(
            sprite = self.exit,
            lst    = self.spawner.group,
            kill   = True,
        ): self.spawner.escaped += 1

        # Draw
        self.bg.clear()
        self.spawner.draw_bg()

        self.window.draw_img(self.bg.current, self.bg.rect)
        self.exit.draw(self.window)
        self.ui.draw()
        self.spawner.draw_screen()
