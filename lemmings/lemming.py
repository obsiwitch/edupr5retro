import enum
import types
import pygame

from shared.collisions import pixel_collision_mid
from shared.animated_sprite import AnimatedSprite, Animations
from lemmings.common import asset_path

STATES = enum.Enum("STATES", "START WALK FALL DEAD")

class Fall:
    def __init__(self, lemming):
        self.lemming = lemming

    def start(self):
        self.lemming.animations.start("FALL")
        self.fallcount = 0

    def run(self):
        self.lemming.rect.move_ip(0, 3)
        self.fallcount += 3
        return (self.fallcount >= 100)

class Walk:
    def __init__(self, lemming):
        self.lemming = lemming

    def start(self):
        self.dx = -1

    def run(self):
        if self.dx < 0: self.lemming.animations.set("WALK_L")
        self.lemming.rect.move_ip(self.dx, 0)

class Dead:
    def __init__(self, lemming):
        self.lemming = lemming

    def start(self):
        self.lemming.animations.start("DEAD")

    def run(self):
        if self.lemming.animations.finished: self.lemming.kill()

class Lemming(AnimatedSprite):
    lemming_imgs = AnimatedSprite.spritesheet_to_images(
        path          = asset_path("planche.png"),
        sprite_size   = (30, 30),
        discard_color = pygame.Color("red"),
    )

    def __init__(self, window):
        self.window = window

        AnimatedSprite.__init__(
            self       = self,
            images     = self.lemming_imgs,
            animations = Animations(
                data = {
                    "WALK_L": range(0, 8),
                    "FALL"  : range(8, 12),
                    "DEAD"  : range(117, 133),
                },
                period  = 100,
            ),
            position = (250, 100)
        )
        self.colorkey(pygame.Color("black"))

        self.actions = types.SimpleNamespace(
            walk = Walk(self),
            fall = Fall(self),
            dead = Dead(self),
        )

        self.state = STATES.START

    def update(self):
        AnimatedSprite.update(self)
        collisions = pixel_collision_mid(
            self.window.screen, self.rect, pygame.Color("black")
        ).invert()

        if self.state == STATES.START:
            self.actions.walk.start()
            self.state = STATES.WALK

        if self.state == STATES.WALK:
            self.actions.walk.run()
            fall = not collisions.down
            if fall:
                self.state = STATES.FALL
                self.actions.fall.start()

        if self.state == STATES.FALL:
            dead = self.actions.fall.run()
            walk = collisions.down
            if dead and walk:
                self.state = STATES.DEAD
                self.actions.dead.start()
            elif not dead and walk:
                self.state = STATES.WALK

        if self.state == STATES.DEAD:
            self.actions.dead.run()
