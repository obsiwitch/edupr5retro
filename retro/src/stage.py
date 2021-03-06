from retro.src.image import Image
from retro.src.sprite import Sprite
from pygame import Rect

class Stage(Sprite):
    # A Stage is a Sprite which can be modified and then restored to its
    # original state (`self.original`). A specific portion of the sprite image
    # can be focused by manipulated `self.camera`.
    def __init__(self, path):
        self.original = Image(path)
        Sprite.__init__(self, self.original.copy())
        self.camera = self.rect.copy()

    ## Transform point `p` from camera space to stage space.
    def camera2stage(self, p):
        return (p[0] + self.camera.x, p[1] + self.camera.y)

    ## Transform point `p` from stage space to camera space.
    def stage2camera(self, p):
        return (p[0] - self.camera.x, p[1] - self.camera.y)

    ## Restore stage to its `self.original` state.
    def clear_all(self):
        self.image.draw_img(self.original, (0, 0))

    ## Restore a portion (`self.camera`) of the stage to its `self.original`
    ## state.
    def clear_focus(self):
        self.image.draw_img(self.original, self.camera.topleft, self.camera)

    def draw(self, target):
        Sprite.draw(self, target, area = self.camera)
