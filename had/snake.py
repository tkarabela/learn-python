import sys
import sdl2
import sdl2.ext
import time


WHITE = sdl2.ext.Color(255, 255, 255)
BLACK = sdl2.ext.Color(0, 0, 0)
RED = sdl2.ext.Color(255, 0, 0)
GREEN = sdl2.ext.Color(0, 255, 0)
BLUE = sdl2.ext.Color(0, 0, 255)


class Screen:
    def __init__(self, name, width: int, height: int, scale: int=1):
        self.width = width
        self.height = height
        self.scale = scale

        sdl2.ext.init()
        self.window = sdl2.ext.Window(name, size=(width*scale, height*scale))

    def show(self):
        self.window.show()

    def refresh(self):
        self.window.refresh()

    def fill(self, color: sdl2.ext.Color):
        sdl2.ext.fill(self.window.get_surface(), color)

    def draw_pixel(self, x: int, y: int, color: sdl2.ext.Color):
        sdl2.ext.fill(self.window.get_surface(), color, area=(self.scale * x,  # x
                                                              self.scale * y,  # y
                                                              self.scale,      # w
                                                              self.scale))     # h


class Game:
    def __init__(self, width: int, height: int):
        self.screen = Screen("Snake", width, height, scale=2)
        self.width = width
        self.height = height
        self.screen.show()
        self.entities = []  # type: list[Entity]
        self.fps = 30.0  # frames per second (approx.)

    def run(self):
        t = 0  # simulation time (number of ticks passed)
        running = True
        while running:
            events = sdl2.ext.get_events()
            running = self.tick(t, events)  # update game state
            self.screen.refresh()  # redraw screen
            time.sleep(1.0/self.fps)  # maintain speed (this assumes that tick() and refresh() are instantaneous)
            t += 1

    def tick(self, t: int, events: list) -> bool:
        # handle game-wide events
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                return False  # exit the game loop

        # clear the screen
        self.screen.fill(BLACK)

        # first, compute intersections before updating any entities
        intersecting_entities_per_entity = []
        for entity in self.entities:
            intersecting_entities = []
            for e in self.entities:
                if e != entity and set(entity.get_coordinates()) & set(e.get_coordinates()):
                    intersecting_entities.append(e)
            intersecting_entities_per_entity.append(intersecting_entities)

        # then, update entities and draw them
        for entity, intersecting_entities in zip(self.entities, intersecting_entities_per_entity):
            entity.tick(t, events, intersecting_entities, self.screen)  # update entity

        # remove dead entities
        self.entities = [e for e in self.entities if e.is_alive()]

        return True  # keep the game running


class Entity:
    def get_coordinates(self):
        raise NotImplementedError

    def is_alive(self):
        raise NotImplementedError

    def tick(self, t: int, events: list, intersecting_entities: list, screen: Screen):
        raise NotImplementedError


class Snake(Entity):
    KEY_TO_MOVE_UP = sdl2.SDLK_w
    KEY_TO_MOVE_DOWN = sdl2.SDLK_s
    KEY_TO_MOVE_LEFT = sdl2.SDLK_a
    KEY_TO_MOVE_RIGHT = sdl2.SDLK_d

    def __init__(self, origin_x, origin_y, length=5, color=WHITE, direction=(0, 1)):
        self.body = [(origin_x, origin_y)]  # list of coordinates ordered from head to tail
        self.length = length  # maximum length to which the snake will grow
        self.direction = direction
        self.color = color

    def get_coordinates(self):
        return self.body

    def is_alive(self):
        return True  # god mode

    def is_intersecting_self(self):
        return len(set(self.body)) != len(self.body)  # has duplicate coordinates in body

    def tick(self, t: int, events: list, intersecting_entities: list, screen: Screen):
        # handle change of direction
        for event in events:
            if event.type == sdl2.SDL_KEYDOWN:
                if event.key.keysym.sym == self.KEY_TO_MOVE_UP:
                    self.direction = (0, -1)
                elif event.key.keysym.sym == self.KEY_TO_MOVE_DOWN:
                    self.direction = (0, +1)
                elif event.key.keysym.sym == self.KEY_TO_MOVE_LEFT:
                    self.direction = (-1, 0)
                elif event.key.keysym.sym == self.KEY_TO_MOVE_RIGHT:
                    self.direction = (+1, 0)

        # move body
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = ((head_x + dx) % screen.width,
                    (head_y + dy) % screen.height)
        self.body.insert(0, new_head)
        while len(self.body) > self.length:
            self.body.pop()

        # handle intersections
        color = self.color
        if self.is_intersecting_self():
            color = RED  # oops, we are eating ourselves
        for e in intersecting_entities:
            if isinstance(e, Snake):
                color = GREEN  # oops, another snake is eating us
            elif isinstance(e, Food):
                self.length += 5  # yay, we ate food

        # draw body
        for x, y in self.body:
            screen.draw_pixel(x, y, color)


class OtherSnake(Snake):
    KEY_TO_MOVE_UP = sdl2.SDLK_UP
    KEY_TO_MOVE_DOWN = sdl2.SDLK_DOWN
    KEY_TO_MOVE_LEFT = sdl2.SDLK_LEFT
    KEY_TO_MOVE_RIGHT = sdl2.SDLK_RIGHT


class Food(Entity):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.alive = True

    def get_coordinates(self):
        return [(self.x, self.y)]

    def is_alive(self):
        return self.alive

    def tick(self, t: int, events: list, intersecting_entities: list, screen: Screen):
        if intersecting_entities:
            self.alive = False  # oops, someone has eaten us
            return

        shade = 100 + 5*(t % 20)
        color = sdl2.ext.Color(shade, shade, shade)
        screen.draw_pixel(self.x, self.y, color)


def main():
    game = Game(300, 200)

    snake = Snake(10, 10)
    other_snake = OtherSnake(40, 10, color=BLUE)
    food = Food(70, 10)

    game.entities.append(snake)
    # game.entities.append(other_snake)
    game.entities.append(food)

    game.run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
