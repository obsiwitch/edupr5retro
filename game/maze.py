import types
import itertools
import retro
from game.assets import assets
from game.collisions import Collisions

class Bonus(retro.Sprite):
    BONUS1 = types.SimpleNamespace(
        id     = 0,
        img    = retro.Image.from_path(assets("bonus1.png")),
        color  = (255, 184, 151),
        value  = 10,
        offset = (0, 0),
    )
    BONUS2 = types.SimpleNamespace(
        id     = 1,
        img    = retro.Image.from_path(assets("bonus2.png")),
        color  = (255, 136, 84),
        value  = 50,
        offset = (-6, -6),
    )

    def __new__(cls, pos, color):
        if   color == cls.BONUS1.color: bonus = cls.BONUS1
        elif color == cls.BONUS2.color: bonus = cls.BONUS2
        else: return None

        self = retro.Sprite.__new__(cls)
        retro.Sprite.__init__(self, bonus.img)
        self.rect.topleft = (
            pos[0] + bonus.offset[0],
            pos[1] + bonus.offset[1],
        )
        self.id = bonus.id
        self.value = bonus.value

        return self

    def __init__(self, pos, color): pass

class Bonuses(list):
    IMG = retro.Image.from_path(assets("bonuses.png"))

    def __init__(self):
        self.count = 0
        list.__init__(self, [])
        for (i, x), (j, y) in Maze.iterator():
            if j == 0: self.append([])
            pos = (x + 6, y + 6)
            b = Bonus(pos, self.IMG[pos])
            self[i].append(b)
            if b: self.count += 1

    def copy(self):
        new = list.__new__(self.__class__)
        new.count = self.count
        list.__init__(new, [lst.copy() for lst in self])
        return new

    def iterator(self):
        for i, line in enumerate(self):
            for j, b in enumerate(line):
                yield i, j, b

    # Search inside growing neighborhoods until a bonus is found.
    def nearest(self, sprite):
        max_reach = max(len(Maze.RANGEW), len(Maze.RANGEH))

        for reach in range(0, max_reach):
            _, _, b = next(self.neighborhood(sprite, reach), (None, None, None))
            if b: return b

        return None

    # Iterator yielding bonuses contained inside a neighborhood centered around
    # `sprite` and defined by a hollow rectangle of a specific `reach`.
    # examples:
    # reach = 0 | reach = 1 | reach = 2
    # ·····     | ·····     | ▫▫▫▫▫
    # ·····     | ·▫▫▫·     | ▫···▫
    # ··▫··     | ·▫s▫·     | ▫·s·▫
    # ·····     | ·▫▫▫·     | ▫···▫
    # ·····     | ·····     | ▫▫▫▫▫
    def neighborhood(self, sprite, reach = 0):
        def inside(i, j): return (
            i in range(len(Maze.RANGEW))
            and j in range(len(Maze.RANGEH))
        )

        i, j = Maze.tile_pos(sprite.rect.center)
        if reach == 0: it = ((0, 0),)
        else: it = itertools.chain(
            itertools.product(range(-reach, reach + 1), (-reach, reach)),
            itertools.product((-reach, reach), range(-reach + 1, reach)),
        )

        for k, l in it:
            k += i ; l += j
            if not inside(k, l): continue
            b = self[k][l]
            if b: yield k, l, b

    def remove(self, i, j):
        self[i][j] = None
        self.count -= 1

    def draw(self, image):
        for _, _, b in self.iterator():
            if b: image.draw_img(b.image, b.rect)

class Walls(list):
    COLOR = (33, 33, 222)

    def __init__(self):
        print("init walls")
        list.__init__(self, [])
        for (i, x), (j, y) in Maze.iterator():
            if j == 0: self.append([])
            pos = (x + 8, y + 8)
            w = Collisions.square3(Maze.IMG, pos, self.COLOR)
            self[i].append(1 if w else 0)

class Maze(retro.Sprite):
    IMG = retro.Image.from_path(assets("maze.png"))
    RANGEW = range(0, IMG.rect().w, 16)
    RANGEH = range(0, IMG.rect().h, 16)
    WALLS = None
    BONUSES = None

    # Defer BONUSES & WALLS initializations to avoid circular dependency
    # problems.
    def __new__(cls):
        if not cls.WALLS: cls.WALLS = Walls()
        if not cls.BONUSES: cls.BONUSES = Bonuses()
        return retro.Sprite.__new__(cls)

    def __init__(self):
        retro.Sprite.__init__(self, self.IMG.copy())
        self.bonuses = self.BONUSES.copy()
        self.walls = self.WALLS

    @classmethod
    def tile_pos(cls, pos): return (pos[0] // 16, pos[1] // 16)

    @classmethod
    def iterator(self, transpose = False):
        it1, it2 = enumerate(self.RANGEW), enumerate(self.RANGEH)
        if transpose: it1, it2 = it2, it1
        for ix, jy in itertools.product(it1, it2):
            if transpose: ix, jy = jy, ix
            yield ix, jy

    # Iterator returning integers each representing an element in the maze.
    def symbols(self, player, ghosts, transpose = False):
        def veq(p1, p2): return (p1[0] == p2[0]) and (p1[1] == p2[1])

        ij_player = self.tile_pos(player.rect.center)

        for (i, _), (j, _) in self.iterator(transpose):
            if veq((i, j), ij_player): yield i, j, 1
            elif self.walls[i][j]: yield i, j, 2
            elif self.bonuses[i][j]: yield i, j, 3
            else: yield i, j, 0

    def draw(self, image):
        retro.Sprite.draw(self, image)
        self.bonuses.draw(image)

    def print(self, player, ghosts):
        symchars = (
            " ", # 0 - floor
            "P", # 1 - player
            "▒", # 2 - wall
            "•", # 3 - bonus
        )

        for i, j, s in self.symbols(player, ghosts, transpose = True):
            if i == 0: print()
            print(symchars[s], end = '')
        print()
