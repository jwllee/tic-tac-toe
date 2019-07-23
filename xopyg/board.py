import numpy as np
import pygame


from xo.utils import *
from xo.board import *
from xopyg.utils import *
from xopyg import color


def draw_board2d(surface, board, color=color.BLACK, padding=5, thickness=2):
    """
    :param padding: screen padding, should be in pixels
    :param thickness: line thickness
    """
    assert_isinstance('Board', Board2d, board)
    width, height = surface.get_size()

    n_rows, n_cols = board.n_rows, board.n_cols

    vlines = np.linspace(padding, width - padding, num=n_rows + 1)
    for i in range(1, n_rows):
        x = vlines[i]
        pygame.draw.line(surface, color, 
                         (x, padding), 
                         (x, height - padding), 
                         thickness)

    hlines = np.linspace(padding, height - padding, num=n_cols + 1)
    for i in range(1, n_cols):
        y = hlines[i]
        pygame.draw.line(surface, color,
                         (padding, y),
                         (width - padding, y),
                         thickness)


class Tile:
    def __init__(self, rect):
        assert_isinstance('Rect', pygame.Rect, rect)
        self.rect = rect

    def draw_marker(self, surface, marker, color=color.BLACK, thickness=2):
        if marker == Marker.CIRCLE:
            self.draw_circle(surface, color, thickness)
        elif marker == Marker.CROSS:
            self.draw_cross(surface, color, thickness)
        else:
            raise ValueError('Do not recognize marker "{!r}"'.format(marker))

    def draw_circle(self, surface, color=color.BLACK, thickness=2):
        # compute the center and radius from the tile's rect
        centerX = self.rect
        center = (centerX, centerY)
        pygame.draw.circle(surface, color, center, radius, thickness)

    def draw_cross(self, surface, color=color.BLACK, thickness=2):
        pass

    def collidepoint(self, x, y):
        return self.rect.collidepoint(x, y)

    def __repr__(self):
        repr_ = 'Tile(x={}, y={}, width={}, height={})'
        x = self.rect.x
        y = self.rect.y
        width = self.rect.width
        height = self.rect.height
        repr_ = repr_.format(x, y, width, height)
        return repr_

    def __str__(self):
        return repr(self)
