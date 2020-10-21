import pygame
from pygame.locals import *
import random
import time


N = 32
BlACK_LINE = 0

class CellLive:
    def __init__(self, time, cell):
        self.time_start = time
        self.cell_state = cell


    def live_and_dead(self):
        if self.cell_state == 2:
            return 2
        elif self.cell_state == 1:
            return 1
        elif self.cell_state == 0:
            return BlACK_LINE


    def time_dead(self):
        return self.time_start

class GameOfLife:
    def __init__(self, width, height, cell_size, speed):
        self.width = width
        self.height = height
        self.cell_size = cell_size

        self.screen_size = width, height
        self.screen = pygame.display.set_mode(self.screen_size)

        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size
        self.speed = speed


    def draw_grid(self):
        i = int()
        for x in range(0, self.width, self.cell_size):
            #pygame.draw.line(self.screen, pygame.Color('red'), (x, 0), (self.height, x), 1)
            pygame.draw.line(self.screen, pygame.Color('red'), (x, 0), (x, self.height), 1)
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('red'), (0, y), (self.width, y), 1)
            #pygame.draw.line(self.screen, pygame.Color('red'), (0, y), (y, self.width), 1)


    def run(self):
        pygame.init()
        run_live_time = time.perf_counter()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))
        list_draw = self.cell_list(True)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_cell_list(list_draw)
            list_draw = self.get_neighbours(list_draw)
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def cell_list(self, randomize=False):
        list_out = list()
        list_per = list()
        if randomize:
            for i in range(N):
                for j in range(N):
                    if i == 0 or j == 0 or i == 31 or j == 31:
                        list_per.append(CellLive(0, BlACK_LINE))
                    else:
                        if random.randint(0, 2) == 1:
                            time_live = time.perf_counter()
                            list_per.append(CellLive(time_live, random.randint(1, 2)))
                        else:
                            list_per.append(CellLive(0, 1))
                list_out.append(list_per)
                del list_per
                list_per = list()
        return list_out


    def draw_cell_list(self, rects):
        index_width = 0
        index_height = 0
        for i in rects:
            for j in i:
                if j.cell_state == 2:
                    pygame.draw.rect(self.screen, pygame.Color('yellow'), (
                    0 + (self.cell_size * index_width), 0 + (self.cell_size * index_height), self.cell_size,
                    self.cell_size))
                elif j.cell_state == BlACK_LINE:
                    pygame.draw.rect(self.screen, pygame.Color('black'), (
                        0 + (self.cell_size * index_width), 0 + (self.cell_size * index_height), self.cell_size,
                        self.cell_size))
                else:
                    pygame.draw.rect(self.screen, pygame.Color('black'), (
                        0 + (self.cell_size * index_width), 0 + (self.cell_size * index_height), self.cell_size,
                        self.cell_size))
                index_width += 1
            index_width = 0
            index_height += 1


    def get_neighbours(self, cell):
        cell_per = list()
        cell_out = list()
        for i in range(N):
            for j in range(N):
                if cell[i][j].cell_state != BlACK_LINE:
                    cell_sum = int(cell[i - 1][j - 1].cell_state + cell[i - 1][j].cell_state + cell[i - 1][j + 1].cell_state + cell[i][j + 1].cell_state + cell[i][j - 1].cell_state +
                        cell[i + 1][j - 1].cell_state + cell[i + 1][j + 1].cell_state + cell[i + 1][j].cell_state) - 8
                    if cell_sum == 3:
                        cell_per.append(CellLive(time.perf_counter(), 2))
                    elif cell_sum == 2:
                        cell_per.append(cell[i][j])
                    elif cell_sum == 0 and (cell[i-1][j-1].cell_state == BlACK_LINE or cell[i][j-1].cell_state == BlACK_LINE or cell[i+1][j+1].cell_state == BlACK_LINE or cell[i][j+1].cell_state == BlACK_LINE):
                        cell_per.append(CellLive(time.perf_counter(), 2))
                    else:
                        cell_per.append(CellLive(0, 1))
                else:
                    cell_per.append(CellLive(0, 0))
            cell_out.append(cell_per)
            del cell_per
            cell_per = list()
        return cell_out


if __name__ == '__main__':
    game = GameOfLife(800, 800, 25, 10)
    game.run()
