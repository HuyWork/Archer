import pygame
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement

class PathFinder:
    def __init__(self, matrix, start, end):
        self.matrix = matrix
        self.grid = Grid(matrix = matrix)
        self.path = []
        self.start = start
        self.end = end

    def create_path(self):
        start_x, start_y = self.start
        start = self.grid.node(start_x // 32, start_y // 32)

        end_x, end_y = self.end
        end = self.grid.node(end_x // 32, end_y // 32)

        finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
        self.path, _ = finder.find_path(start, end, self.grid)
        self.grid.cleanup()
    
    def draw_path(self, screen):
        if self.path: 
            points = []
            for point in self.path:
                x = (point[0] * 32) + 16
                y = (point[1] * 32) + 16
                points.append((x, y))
            pygame.draw.lines(screen, '#4a4a4a', False, points, 5)
    
    def update(self):
        self.draw_path()

class Path():
    def __init__(self, rect, empty_path):
        #basic
        self.rect = rect

        #movent
        self.pos = self.rect.center
        self.speed = 3
        self.direction = pygame.math.Vector2(0,0)

        #path
        self.path = []
        self.collision_rects = []
        self.empty_path = empty_path

    def get_coord(self):
        col = self.rect.centerx
        row = self.rect.centery
        return (col, row)
    
    def set_path(self, path):
        self.path = path
        self.create_collision_rects()
        self.get_direction()

    def create_collision_rects(self):
        if self.path:
            self.collision_rects = []
            for point in self.path:
                x = (point[0] * 32) + 16
                y = (point[1] * 32) + 16
                rect = pygame.Rect((x - 2, y - 2),(4, 4))
                self.collision_rects.append(rect)
    
    def get_direction(self):
        if self.collision_rects:
            start = pygame.math.Vector2(self.pos)
            end = pygame.math.Vector2(self.collision_rects[0].center)
            self.direction = (end - start).normalize()
        else:
            self.direction = pygame.math.Vector2(0,0)
            self.path = []

    def check_collisions(self):
        if self.collision_rects:
            for rect in self.collision_rects:
                if rect.collidepoint(self.pos):
                    del self.collision_rects[0]
                    self.get_direction()
        else:
            self.empty_path()

    def move(self):
        self.pos += self.direction * self.speed
        self.check_collisions()
        self.rect.center = self.pos
    
    def update(self):
        self.move()