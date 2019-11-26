import sys
import sdl2
import sdl2.ext
import time


FPS = 30

def run():
    sdl2.ext.init()
    window = sdl2.ext.Window("The Pong Game", size=(800, 600))
    window.show()
    running = True

    x = sdl2.ext.pixels2d(window.get_surface())
    print(x, repr(x), x.shape)
    x = sdl2.ext.pixels3d(window.get_surface())
    print(x, repr(x), x.shape)

    i = 0

    while running:
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
        window.refresh()
        time.sleep(1.0/FPS)

        x[i,i] = [255, 128, 64, 0]

        if i %10==0:
            sdl2.ext.fill(window.get_surface(), sdl2.ext.Color(0,0,0))

        i += 1
        print(123)
    return 0

if __name__ == "__main__":
    sys.exit(run())