# Pygame Of Life

Implementation of Conway's "Game Of Life" in less than 100 (ignoring the added interactivity features)
lines of modern Python.

![](https://raw.githubusercontent.com/matheusgomes28/pygame-life/main/media/pygame-of-life.gif)

The engine is entirely and purely implemented using vanilla
Python 3.9, and [Pygame](https://www.pygame.org/) is used for
the graphics front.

## Running The Game

I recommend using the latest version of Python (3.9) on a
separate environment to your normal development one. Two
good options are Anaconda or Virtualenv, just create a new
environment for this game and install the dependencies with:

```shell
pip install -r requirements.txt
```

Given that all the dependencies were installed, running the
game is as simple as

```shell
python pygame_life.py
```

## Understand The Code

This game was created for a post in my  personal blog.
The intention was to show that, by keeping it simple, [Conway's Game Of Life 
can be implemented in a few lines of Python](https://matgomes.com/conways-game-of-life-python).

Interactivty by skd988.

## Interactivity
### Mouse:
Left click - set cell (alive)

Right click - clear cell (dead)

Middle click - toggle cell

### Keyboard:
Space - play/pause

C - clear all cells (dead)

Up Arrow - increase speed

Down Arrow - decrease speed

Right Arrow - advance one update (while paused)