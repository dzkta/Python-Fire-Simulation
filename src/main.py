import sys
from random import randint

import pygame
from pygame.math import Vector2

WIN_SIZE: tuple[int, int] = (600, 600)
TITLE: str = "Fire Simulation - by dzKTA"
FPS: int = 10
CELL_W: int = 10 # Recommended 5 - 20
CELL_SIZE: tuple[int, int] = (CELL_W, CELL_W)
GRID_SIZE: tuple[int, int] = (WIN_SIZE[0] // CELL_SIZE[0], WIN_SIZE[1] // CELL_SIZE[1])
FIRE_FADEOUT: int = CELL_SIZE[0] # Recommended
FIRE_STEP_VALUES: tuple = (245, 128)

class Cell(pygame.sprite.Sprite):

    def __init__(self, pos: Vector2, val: int, *groups: pygame.sprite.Group) -> None:
        super().__init__(*groups)

        if val in range(255 + 1):
            self.val = val
        else:
            self.val = 1

        self.color = self._calculate_color_from_value(self.val)

        self.image = pygame.Surface(CELL_SIZE)
        self.image.fill(self.color)
        self.rect = self.image.get_rect(topleft=pos)

    def update_color(self):
        self.color = self._calculate_color_from_value(self.val)
        self.image.fill(self.color)

    def update(self):
        self.update_color()

    @staticmethod
    def _calculate_color_from_value(val: int) -> tuple[int, int, int]:
        val = max(0, min(255, val))

        if val >= FIRE_STEP_VALUES[0]:
            t = (val - 128) / 127
            r = 255
            g = int(128 + 127 * t)
            b = int(192 + 63 ** t)
        elif val >= FIRE_STEP_VALUES[1] and val < FIRE_STEP_VALUES[0]:
            t = (val - 128) / 127
            r = 255
            g = int(128 + 127 * t)
            b = int(255 * t)
        else:
            t = val / 128
            r = int(255 * t)
            g = int(120 ** t)
            b = 0

        return (r, g, b)

# Handles logic of the simulation
class Logic:

    def __init__(self) -> None:
        self.visible_sprites = pygame.sprite.Group()

        self.grid: list[list[Cell | None]] = []
        for y in range(GRID_SIZE[1]):
            self.grid.append([])
            for x in range(GRID_SIZE[0]):
                self.grid[y].append(Cell(
                    Vector2(x * CELL_SIZE[0], y * CELL_SIZE[1]),
                    255 if y == GRID_SIZE[1] - 1 else 0,
                    self.visible_sprites
                ))

        self.wind = 0

    def spread_cells(self):
        for idx_y in range(len(self.grid) - 2, -1, -1):
            for idx_x, cell in enumerate(self.grid[idx_y]):
                rx = randint(
                    max(0, idx_x - 1),
                    min(GRID_SIZE[0] - 1, idx_x + 1)
                )

                prev_val = self.grid[idx_y + 1][rx].val
                cell.val = max(0, prev_val - randint(1, FIRE_FADEOUT))

    def update(self):
        self.visible_sprites.update()
        self.spread_cells()

class Main:

    def __init__(self) -> None:
        pygame.init()

        self.win = pygame.display.set_mode(WIN_SIZE)
        pygame.display.set_caption(TITLE)

        self.clock = pygame.time.Clock()
        self.fps = FPS

        self.on_run: bool = False

        self.logic = Logic()

    def update(self):
        self.logic.update()

    def render(self):
        # self.win.fill((25, 25, 25))
        self.logic.visible_sprites.draw(self.win)

        pygame.display.update()

    def run(self):
        self.on_run = True
        while self.on_run:
            self.clock.tick(self.fps)

            self.handle_events()

            self.update()
            self.render()

        pygame.quit()
        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.on_run = False

if __name__ == "__main__":
    main = Main()
    main.run()
