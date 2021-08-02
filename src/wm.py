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

import pygame
import ngcf
from typing import List
from draw import NodeTreeDraw
pygame.init()


class WindowManager:
    """Manages sections on the display."""

    _tree_stack: List[ngcf.NodeTree]
    _draw_stack: List[NodeTreeDraw]

    def __init__(self):
        self._tree_stack = []
        self._draw_stack = []

        self.push(ngcf.NodeTree())
        self._tree_stack[-1].add_node(ngcf.available_nodes()[0]())

    def push(self, tree: ngcf.NodeTree) -> None:
        """
        Add a tree to the stack.
        """
        self._tree_stack.append(tree)
        self._draw_stack.append(NodeTreeDraw(tree))

    def pop(self) -> ngcf.NodeTree:
        """
        Remove from the top of the stack.
        """
        self._draw_stack.pop()
        return self._tree_stack.pop()

    def draw(self, surface: pygame.Surface, events) -> None:
        draw = self._draw_stack[-1]
        surf = draw.draw(events, surface.get_size())
        surface.blit(surf, (0, 0))
