import pygame
from pygame.locals import *
import random
from pprint import pprint as pp

N = 32
BlACK_LINE = 0

class GameOfLife:
    def __init__(self, width, height, cell_size, speed):
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size
        # Скорость протекания игры
        self.speed = speed


    def draw_grid(self):
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('white'),(x, 0), (x, self.height), 1)
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('white'),(0, y), (self.width, y), 1)


    def run(self):
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))
        list_draw = self.cell_list(True)
        #self.draw_cell_list(list_draw)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_cell_list(list_draw)
            #self.draw_grid()
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
                        list_per.append(BlACK_LINE)
                    else:
                        if random.randint(0, 2) == 1:
                            list_per.append(random.randint(1, 2))
                        else:
                            list_per.append(1)
                list_out.append(list_per)
                del list_per
                list_per = list()
        return list_out


    def draw_cell_list(self, rects):
        index_width = 0
        index_height = 0
        for i in rects:
            for j in i:
                if j == 2:
                    pygame.draw.rect(self.screen, pygame.Color('yellow'), (0+(self.cell_size * index_width), 0 + (self.cell_size * index_height), self.cell_size, self.cell_size))
                elif j == BlACK_LINE:
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
                if cell[i][j] != BlACK_LINE:
                    cell_sum = int(cell[i - 1][j - 1] + cell[i - 1][j] + cell[i - 1][j + 1] + cell[i][j + 1] + cell[i][j - 1] +
                        cell[i + 1][j - 1] + cell[i + 1][j + 1] + cell[i + 1][j]) - 8
                    if cell_sum == 3:
                        cell_per.append(2)
                    elif cell_sum == 2:
                        cell_per.append(cell[i][j])
                    elif cell_sum == 0 and (cell[i-1][j-1]== BlACK_LINE or cell[i][j-1]== BlACK_LINE or cell[i+1][j+1]== BlACK_LINE or cell[i][j+1]== BlACK_LINE):
                        cell_per.append(2)
                    else:
                        cell_per.append(1)
                else:
                    cell_per.append(BlACK_LINE)
            cell_out.append(cell_per)
            del cell_per
            cell_per = list()
        return cell_out


if __name__ == '__main__':
    game = GameOfLife(800, 800, 25, 10)
    clist = game.cell_list(True)
    for i in clist:
        print(i)
    print()
    rek = game.get_neighbours(clist)
    for i in rek:
        print(i)
    game.draw_cell_list(clist)
    game.run()