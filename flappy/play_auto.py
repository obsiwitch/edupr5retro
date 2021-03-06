from retro.src import retro
from flappy.game import Game

window = retro.Window(title='Flappy Bird', size=(288, 512), fps=100)

game = Game(window, nbirds = 1)

def update():
    if not game.finished:
        b = game.birds[0]
        if game.target.centery - b.rect.y < 0: b.flap()
        game.update()
    else:
        game.reset()

window.loop(update, game.render)
