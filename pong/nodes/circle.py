from retro.src import retro

class Circle:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    @property
    def x(self): return self.center[0]
    @x.setter
    def x(self, v): self.center[0] = v

    @property
    def y(self): return self.center[1]
    @y.setter
    def y(self, v): self.center[1] = v

    @property
    def top(self): return (self.center[1] - self.radius)
    @top.setter
    def top(self, v): self.center[1] = v + self.radius

    @property
    def bottom(self): return (self.center[1] + self.radius)
    @bottom.setter
    def bottom(self, v): self.center[1] = v - self.radius

    @property
    def left(self): return (self.center[0] - self.radius)
    @left.setter
    def left(self, v): self.center[0] = v + self.radius

    @property
    def right(self): return (self.center[0] + self.radius)
    @right.setter
    def right(self, v): self.center[0] = v - self.radius

    # Returns  1 when `self`'s right side collides `rect`'s left side.
    # Returns -1 when `self`'s left side collides `rect`'s right side.
    # Returns  0 when no collision happens.
    def collide(self, shape):
        if isinstance(shape, retro.Rect):
            right = shape.collidepoint(self.right, self.y)
            left  = shape.collidepoint(self.left, self.y)
            return (right - left)
        else:
            raise NotImplementedError
