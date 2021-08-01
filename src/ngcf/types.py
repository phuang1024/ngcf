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

from typing import Any, List, Tuple, Union


class Socket:
    """Base node socket."""
    name: str
    default: Any

    # These are updated by the node tree
    value: Any
    connection: Union[None, Tuple[int, int]]

    def __init__(self):
        self.connection = None

    def set_value(self, value: Any) -> None:
        self.value = value

class SocketBool(Socket):
    """Boolean socket."""

    def __init__(self, name: str = "", default: bool = False) -> None:
        super().__init__()
        self.name = name
        self.default = default

class SocketInt(Socket):
    """Integer socket."""

    min: int
    max: int

    def __init__(self, name: str = "", default: int = 0, min: int = int(-1e9), max: int = int(1e9)) -> None:
        super().__init__()
        self.name = name
        self.default = default
        self.min = min
        self.max = max

    def set_value(self, value: int) -> None:
        self.value = max(min(value, self.max), self.min)

class SocketFloat(Socket):
    """Float64 socket."""

    min: float
    max: float

    def __init__(self, name: str = "", default: float = 0, min: float = -1e9, max: float = 1e9) -> None:
        super().__init__()
        self.name = name
        self.default = default
        self.min = min
        self.max = max

    def set_value(self, value: float) -> None:
        self.value = max(min(value, self.max), self.min)

class SocketStr(Socket):
    """String socket."""

    max_len: int

    def __init__(self, name: str = "", default: float = 0, max_len: int = int(1e4)) -> None:
        super().__init__()
        self.name = name
        self.default = default
        self.max_len = max_len

    def set_value(self, value: str) -> None:
        self.value = value[:self.max_len]


class Node:
    """
    Base node class.
    Inherit from this to create your custom node.
    """
    inputs: List[Socket]
    outputs: List[Socket]

    id_num: int


class NodeTree:
    """
    A node tree manager.
    """
    nodes: List[Node]

    def __init__(self):
        self.nodes = []
        self.next_id = 0

    def add_node(self, node: Node) -> int:
        """
        Add a new node.

        :return: The new node's ID number.
        """
        id_num = self.next_id
        node.id_num = id_num
        self.nodes.append(node)

        self.next_id += 1
        return id_num

    def rm_node(self, id_num: int) -> None:
        """
        Removes node and all it's connections.
        """
        ind = self.get_node_index_by_id(id_num)
        node = self.nodes[ind]

        for inp in node.inputs:
            if inp.connection is not None:
                i, sock = inp.connection
                self.nodes[i].outputs[sock].connection = None
        for out in node.outputs:
            if out.connection is not None:
                i, sock = out.connection
                self.nodes[i].inputs[sock].connection = None

        self.nodes.pop(ind)

    def get_node_by_id(self, id_num: int) -> Node:
        """
        Get node by id number.
        """
        for node in self.nodes:
            if node.id_num == id_num:
                return node
        raise ValueError(f"No node with ID {id_num}")

    def get_node_index_by_id(self, id_num: int) -> int:
        """
        Get node index by id number.
        """
        for i, node in enumerate(self.nodes):
            if node.id_num == id_num:
                return i
        raise ValueError(f"No node with ID {id_num}")

    def make_connection(self, out_node_id: int, out_socket_num: int, in_node_id: int,
            in_socket_num: int) -> None:
        """
        Makes a connection between two nodes.

        :param out_node_id: Output node id.
        :param out_socket_num: Output node socket number.
        :param in_node_id: Input node id.
        :param in_socket_num: Input node socket number.
        """
        out_socket = self.get_node_by_id(out_node_id).outputs[out_socket_num]
        in_socket = self.get_node_by_id(in_node_id).inputs[in_socket_num]

        out_socket.connection = (in_node_id, in_socket_num)
        in_socket.connection = (out_node_id, out_socket_num)
