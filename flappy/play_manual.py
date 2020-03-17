import retro
from game import Game

window = retro.Window(
    title = "Flappy Bird",
    size  = (288, 512),
)

game = Game(window, nbirds = 1)

def main():
    if not game.finished:
        b = game.birds[0]
        if window.events.key_press(retro.K_SPACE): b.flap()
        game.run()
    else:
        game.reset()

window.loop(main)