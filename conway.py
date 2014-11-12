#!/usr/bin/env python3

from itertools import chain
from PIL import Image, ImageChops
from PIL.GifImagePlugin import getheader, getdata

def make_neighbors(point):
    x, y = point
    for dx in [1, 0, -1]:
        for dy in [1, 0, -1]:
            if dx or dy:
                yield (x + dx, y + dy)

def tick(world):
    new_world = set()

    for point in world | set(chain(*map(make_neighbors, world))):
        living = point in world
        neighbors = sum(1 for neighbor in make_neighbors(point) if neighbor in world)

        # Any live cell with fewer than two live neighbours dies, as if caused by under-population.
        # Any live cell with two or three live neighbours lives on to the next generation.
        if living and 2 <= neighbors <= 3:
            new_world.add(point)

        # Any live cell with more than three live neighbours dies, as if by overcrowding.
        # Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
        if not living and neighbors == 3:
            new_world.add(point)

    return new_world

def read_pattern(s):
    world = set()

    lines = [line for line in s.splitlines() if not line.startswith("!")]

    for x, line in enumerate(lines):
        for y, c in enumerate(line):
            if not c.isspace() and not c == ".":
                world.add((x, y))

    return world

def move(world, dx=0, dy=0):
    return {(x + dx, y + dy) for x, y in world}

def print_world(world, x0=0, y0=0, w=40, h=20, living="x", dead=" "):
    print((w+2) * "-")
    for x in range(x0, x0+h):
        print("|", end="")
        for y in range(y0, y0+w):
            print(living if (x, y) in world else dead, end="")
        print("|")
    print((w+2) * "-")

def print_world_to_image(world, x0=0, y0=0, w=100, h=100, living=0, dead=1):
    im = Image.new("1", (w, h), dead)

    for x in range(x0, x0+h):
        for y in range(y0, y0+w):
            if (x, y) in world:
                im.putpixel((x, y), living)

    return im

######################

GLIDER = read_pattern("""
!Name: Glider
!Author: Richard K. Guy
!The smallest, most common, and first discovered spaceship.
!www.conwaylife.com/wiki/index.php?title=Glider
.O
..O
OOO
""")

BEACON = read_pattern("""
!Name: Beacon
!Author: John Conway
!The third most common oscillator (after the blinker and toad).
!www.conwaylife.com/wiki/index.php?title=Beacon
OO
O
...O
..OO
""")

DART = read_pattern("""
!Name: Dart
!Author: David Bell
!A period 3 spaceship with speed c/3 that was found in May 1992.
!www.conwaylife.com/wiki/index.php?title=Dart
.......O
......O.O
.....O...O
......OOO

....OO...OO
..O...O.O...O
.OO...O.O...OO
O.....O.O.....O
.O.OO.O.O.OO.O
""")

GOSPER_GLIDER_GUN = read_pattern("""
!Name: Gosper glider gun
!Author: Bill Gosper
!The first known gun and the first known finite pattern with unbounded growth.
!www.conwaylife.com/wiki/index.php?title=Gosper_glider_gun
........................O
......................O.O
............OO......OO............OO
...........O...O....OO............OO
OO........O.....O...OO
OO........O...O.OO....O.O
..........O.....O.......O
...........O...O
............OO
""")

######################

# code from
# https://github.com/python-pillow/Pillow/blob/master/Scripts/gifmaker.py

def makedelta(fp, sequence):
    """Convert list of image frames to a GIF animation file"""

    frames = 0
    previous = None

    for im in sequence:
        #
        # FIXME: write graphics control block before each frame

        if not previous:
            # global header
            for s in getheader(im)[0]:
                fp.write(s)
            for s in getdata(im):
                fp.write(s)
        else:
            # delta frame
            delta = ImageChops.subtract_modulo(im, previous)
            bbox = delta.getbbox()

            if bbox:
                # compress difference
                for s in getdata(im.crop(bbox), offset = bbox[:2]):
                    fp.write(s)
            else:
                # FIXME: what should we do in this case?
                pass

        previous = im.copy()
        frames += 1

    fp.write(b";")
    return frames

######################

def main():
    world = GLIDER | move(GLIDER, 30, 30) | move(BEACON, 5, 5) | move(GOSPER_GLIDER_GUN, 50, 50)
    steps = 150
    images = []

    for t in range(steps):
        print("t =", t)
        # print_world(world)
        im = print_world_to_image(world)
        im = im.resize([4*d for d in im.size], Image.NEAREST)
        images.append(im)
        world = tick(world)

    with open("conway.gif", "wb") as fp:
        makedelta(fp, images)

if __name__ == "__main__":
    main()
