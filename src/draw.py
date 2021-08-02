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
from typing import List, Tuple
pygame.init()


class NodeTreeDraw:
    """Draws a node tree."""

    view: List[float]
    zoom: float
    tree: ngcf.NodeTree

    def __init__(self, tree: ngcf.NodeTree):
        self.view = [0, 0]
        self.zoom = 1
        self.tree = tree

    def draw(self, events, size: Tuple[float, float]) -> pygame.Surface:
        surf = pygame.Surface(size)
        for node in self.tree.nodes:
            loc = (self.view[0]+node.loc[0], self.view[1]+node.loc[1])
            draw_node(surf, node, (255, 0, 0), loc)

        return surf


def draw_node(surface: pygame.Surface, node: ngcf.Node, color: Tuple[int, int, int], loc: Tuple[float, float]) -> None:
    """
    Draw a node on the surface.

    :param surface: Pygame surface.
    :param node: Node.
    :param color: Node header color.
    :param loc: (X, Y) location on the surface.
    """
    pygame.draw.rect(surface, (150, 150, 150), (*loc, 150, 200))
    pygame.draw.rect(surface, color, (*loc, 150, 20))
