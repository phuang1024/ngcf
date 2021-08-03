#
#  ngcf
#  Node-based general computing framework.
#  Copyright Patrick Huang 2021
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import colorsys
import pygame
import ngcf
import events
from typing import List, Tuple
pygame.init()


class NodeTreeDraw:
    """Draws a node tree."""

    grid_size = 20

    view: List[float]
    zoom: float
    tree: ngcf.NodeTree

    def __init__(self, tree: ngcf.NodeTree):
        self.view = [0, 0]
        self.zoom = 1
        self.tree = tree

    def draw(self, loc: Tuple[float, float], size: Tuple[float, float]) -> pygame.Surface:
        surf = pygame.Surface(size, pygame.SRCALPHA)
        surf.fill((40, 40, 40))

        # Draw grid
        x = (self.view[0]%self.grid_size) - self.grid_size
        y = (self.view[1]%self.grid_size) - self.grid_size
        while (x <= size[0]) or (y <= size[1]):
            pygame.draw.line(surf, (30, 30, 30), (x, 0), (x, size[1]))
            pygame.draw.line(surf, (30, 30, 30), (0, y), (size[0], y))
            x += self.grid_size
            y += self.grid_size

        # Draw nodes
        for node in self.tree.nodes:
            loc = (self.view[0]+node.loc[0], self.view[1]+node.loc[1])
            draw_node(surf, node, (255, 0, 0), loc)

        # Draw selection box
        if events.mouse_drag[0]:
            loc1 = [loc[i]+events.mouse_drag_start[0][i] for i in range(2)]
            loc2 = [loc[i]+events.mouse_drag_end[0][i] for i in range(2)]
            x, y = min(loc1[0], loc2[0]), min(loc1[1], loc2[1])
            w, h = abs(loc1[0]-loc2[0]), abs(loc1[1]-loc2[1])

            subsurf = pygame.Surface((w, h), pygame.SRCALPHA)
            subsurf.fill((255, 255, 255, 25))
            surf.blit(subsurf, (x, y))
            pygame.draw.rect(surf, (255, 255, 255), (x, y, w, h), 1)

        return surf


def draw_node(surface: pygame.Surface, node: ngcf.Node, color: Tuple[int, int, int], loc: Tuple[float, float]) -> None:
    """
    Draw a node on the surface.

    :param surface: Pygame surface.
    :param node: Node.
    :param color: Node header color.
    :param loc: (X, Y) location on the surface.
    """
    pygame.draw.rect(surface, (90, 90, 90), (*loc, 150, 200))
    pygame.draw.rect(surface, color, (*loc, 150, 20))

    if node.selected:
        pygame.draw.rect(surface, (255, 255, 255), (*loc, 150, 200), 1)
