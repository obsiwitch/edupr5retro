import pygame
class Rect(pygame.Rect):
    # Constructeur

    ## Rect(int left, int top, int width, int height) -> Rect
    ## Rect(2-tuple topleft, 2-tuple size) -> Rect
    ## Rect(Rect rect) -> Rect
    def __init__(self, *args):
        pygame.Rect.__init__(self, args)

    # Méthodes

    ## copy() -> Rect
    ## Retourne un nouveau rectangle possédant la même position et la même
    ## taille que l'original.
    def copy(self): return pygame.Rect.copy(self)

    ## Move(2-tuple v)
    ## Move(int x, int y)
    ## Déplace le rectangle de `x` et `y`.
    def move(self, *v): pygame.Rect.move_ip(self, v) ; return self

    ## clamp(Rect rect)
    ## Déplace le rectangle actuel dans `rect`. Si le rectangle actuel est trop
    ## grand pour rentrer dans `rect`, il sera centré à l'intérieur et sa taille
    ## ne changera pas.
    def clamp(self, rect): pygame.Rect.clamp_ip(self, rect) ; return self

    ## union(Rect rect) -> Rect
    ## Retourne un nouveau rectangle étant l'union du rectangle actuel et de
    ## `rect`.
    def union(self, rect): return pygame.Rect.union(self, rect)

    ## union(Rect rect) -> Rect
    ## Retourne un nouveau rectangle étant l'intersection du rectangle actuel et
    ## de `rect`.
    def intersection(self, rect): return pygame.Rect.clip(self, rect)

    ## contains(Rect rect) -> bool
    ## Teste si `rect` est complétement à l'intérieur du rectangle actuel.
    def contains(self, rect): return pygame.Rect.contains(self, rect)

    ## collidepoint(2-tuple p) -> bool
    ## collidepoint(int x, int y) -> bool
    ## Teste si `p` est à l'intérieur du rectangle actuel.
    def collidepoint(self, *p): return pygame.Rect.collidepoint(self, p)

    ## colliderect(Rect rect) -> bool
    ## Teste s'il y intersection entre `rect` et le rectangle actuel.
    def colliderect(self, rect): return pygame.Rect.colliderect(self, rect)

    # Propriétés

    ## Plusieurs propriétés permettent de bouger et d'aligner le rectangle.
    ## ~~~
    ## x, y
    ## top, left, bottom, right
    ## topleft, bottomleft, topright, bottomright
    ## midtop, midleft, midbottom, midright
    ## center, centerx, centery
    ## size, width, height, w, h
    ## ~~~

    __lt__ = property()
    __le__ = property()
    __gt__ = property()
    __ge__ = property()
    move_ip = property()
    inflate = property()
    inflate_ip = property()
    clamp_ip = property()
    clip = property()
    union_ip = property()
    unionall = property()
    unionall_ip = property()
    fit = property()
    normalize = property()
    collidelist = property()
    collidelistall = property()
    collidedict = property()
    collidedictall = property()
