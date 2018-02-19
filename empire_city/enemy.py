import random
import enum
import pygame

from shared.sprite import Sprite
from shared.timer  import Timer
from empire_city.common import asset_path

# Enemy generator.
class Enemies:
    street_images = Sprite.path_to_images([
            asset_path("bandit_rue.png"),
            asset_path("bandit_rue2.png"),
            asset_path("bandit_rue4.png")
    ])

    window_images = Sprite.path_to_images([
        asset_path("bandit_window.png"),
        asset_path("bandit_window2.png"),
        asset_path("bandit_window3.png"),
        asset_path("bandit_window4.png"),
    ])

    wall_images = Sprite.path_to_images([
        asset_path("bandit_mur.png"),
        asset_path("bandit_mur2.png"),
    ])

    top_images = Sprite.path_to_images([
        asset_path("bandit_appui.png"),
        asset_path("bandit_appui2.png"),
        asset_path("bandit_appui3.png"),
    ])

    sewer_image = Sprite.path_to_image(
        asset_path("bandit_egout.png"),
    )

    kidnaper_image = Sprite.path_to_image(
        asset_path("woman.png"),
    )

    runner_image = Sprite.path_to_image(
        asset_path("bandit_rue3.png"),
    )

    def __init__(self, camera):
        self.camera = camera
        self.bg = camera.bg

        self.generators = (
            self.new_street_mob,
            self.new_window_mob,
            self.new_wall_mob,
            self.new_top_mob,
            self.new_sewer_mob,
            self.new_kidnaper_mob,
            self.new_runner_mob,
        )

        self.next()
        self.mob.alive = False

        self.repop_timer = Timer(3)

    def street_position(self, sprite):
        sprite.rect.bottom = self.bg.rect.bottom - 10
        sprite.rect.left = random.randint(100, self.bg.rect.width - 100)

    def new_street_mob(self):
        mob = Enemy(self.camera, random.choice(self.street_images))
        self.street_position(mob)
        return mob

    def new_window_mob(self):
        i = random.randrange(len(self.window_images))
        positions = ((1244, 78), (1312, 258), (952, 84), (790, 88))
        mob = Enemy(self.camera, self.window_images[i])
        mob.rect.topleft = positions[i]
        return mob

    def new_wall_mob(self):
        positions = ((710, 600), (1140, 600), (1823, 600))
        mob = Enemy(self.camera, random.choice(self.wall_images))
        mob.rect.bottomright = random.choice(positions)
        return mob

    def new_top_mob(self):
        positions = ((29, 191), (356, 191), (1712, 411))
        mob = Enemy(self.camera, random.choice(self.top_images))
        mob.rect.midbottom = random.choice(positions)
        return mob

    def new_sewer_mob(self):
        mob = Enemy(self.camera, self.sewer_image)
        mob.rect.topleft = (410, 642)
        return mob

    def new_kidnaper_mob(self):
        mob = Kidnaper(self.camera, self.kidnaper_image)
        self.street_position(mob)
        return mob

    def new_runner_mob(self):
        mob = Runner(self.camera, self.runner_image)
        self.street_position(mob)
        return mob

    def next(self):
        self.mob = random.choice(self.generators)()

    def kill(self, p):
        killed = self.mob.kill(p)
        if killed: self.repop_timer.restart()
        return killed

    def update(self, target):
        repop = (
            not self.mob.alive
            and self.repop_timer.finished
        )
        if repop: self.next()

        self.mob.update(target)

    def draw_bg(self):
        self.mob.draw_bg()

    def draw_screen(self):
        self.mob.draw_screen()

class Enemy(Sprite):
    def __init__(self, camera, image):
        Sprite.__init__(self, image)

        self.camera = camera
        self.window = camera.window
        self.bg     = camera.bg

        self.alive = True
        self.shoot_timer = Timer(3)

    def kill(self, p):
        killed = (self.alive and self.rect.collidepoint(p))
        if killed: self.alive = False
        return killed

    def shoot(self, target):
        if not self.shoot_timer.finished: return
        self.shoot_timer.restart()
        if target.hidden: return
        target.ammunitions -= 3

    def update(self, target):
        if not self.alive: return
        self.shoot(target)

    def draw_shoot_timer(self):
        if not self.alive: return

        shoot_timer_surface = self.window.fonts[1].render(
            f"{self.shoot_timer.remaining}", # text
            False,                           # antialias
            pygame.Color("white")            # color
        )
        self.window.screen.blit(
            shoot_timer_surface,
            shoot_timer_surface.get_rect(
                midbottom = self.window.rect.midbottom
            ).move(0, 0)
        )

    def draw_bg(self):
        if not self.alive: return
        self.draw(self.bg.image)

    def draw_screen(self):
        if not self.alive: return
        self.draw_shoot_timer()

class Kidnaper(Enemy):
    def __init__(self, camera, image):
        Enemy.__init__(self, camera, image)

    def kill(self, p):
        kidnaper = self.rect.copy()
        kidnaper.width //= 2
        victim = self.rect.copy()
        victim.width //= 2
        victim.x += victim.width

        victim_killed   = (self.alive and victim.collidepoint(p))
        kidnaper_killed = (self.alive and kidnaper.collidepoint(p))
        if victim_killed or kidnaper_killed: self.alive = False
        return (kidnaper_killed - victim_killed)

class Runner(Enemy):
    def __init__(self, camera, image):
        Enemy.__init__(self, camera, image)
        self.dx = -2

    def move(self):
        self.rect.x += self.dx
        if not self.bg.rect.contains(self.rect):
            self.rect.clamp_ip(self.bg.rect)
            self.dx *= -1

    def update(self, target):
        Enemy.update(self, target)
        self.move()
