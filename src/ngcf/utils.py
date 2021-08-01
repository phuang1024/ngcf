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

__all__ = (
    "register_node",
    "available_nodes",
)

from typing import List
from .nodes import Node

_available_nodes = []


def register_node(node: Node) -> None:
    """
    Add a node.
    """
    _available_nodes.append(node)

def available_nodes() -> List[Node]:
    """
    Returns all available nodes.
    """
    return _available_nodes
