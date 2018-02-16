import enum

import pygame

from shared.window  import Window
from maze.state_run import StateRun
from maze.state_end import StateEnd

window = Window(
    width  = 400,
    height = 400,
    title  = "Maze"
)

State = enum.Enum("State", "START RUN END")
state = State.START

state_run = None
state_end = None

def game():
    global state
    global state_run
    global state_end

    if state == State.START:
        state_run = StateRun(window)
        state = State.RUN

    if state == State.RUN:
        win = state_run.run()
        if win:
            del state_run
            state_end = StateEnd(window)
            state = State.END

    elif state == State.END:
        restart = state_end.run()
        if restart:
            del state_end
            state_run = StateRun(window)
            state = State.RUN

window.loop(game)
