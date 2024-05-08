import pygame
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from settings import *

class PathFinder:
    def __init__(self, start, end):
        self.matrix = Map.MATRIX
        self.grid = Grid(matrix = self.matrix)
        self.start, self.end = start, end

        self.path = []
        self.collision_rects = []

    # hàm tạo ra đường cho enemy đi
    def create_path(self, diagonal_movement):
        start_x, start_y = self.start
        start = self.grid.node(start_x // 32, start_y // 32)

        end_x, end_y = self.end
        end = self.grid.node(end_x // 32, end_y // 32)

        finder = AStarFinder(diagonal_movement = diagonal_movement)
        self.path, _ = finder.find_path(start, end, self.grid)
        self.grid.cleanup()
        return self.path
    
    # tạo ra các rect cho mỗi ô trên ma trận để enemy xác định hướng đi
    def create_collision_rects(self):
        if self.path:
            for point in self.path:
                x = (point.x * 32) + 16
                y = (point.y * 32) + 16
                rect = pygame.Rect((x - 2, y - 2),(4, 4))
                self.collision_rects.append(rect)
        return self.collision_rects