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
    "Node",
    "NodeTree",
)

from typing import Any, List, Sequence, Tuple
from .sockets import Socket


class Node:
    """
    Base node class.
    Inherit from this to create your custom node.

    Define:

    * ``inputs``: List of input sockets.
    * ``outputs``: List of output sockets.
    * ``name``: Node name which will show up in the GUI.
    * ``category``: Node category.
    """
    inputs: Sequence[Socket]
    outputs: Sequence[Socket]

    name: str
    category: str

    # Updated by node tree and/or GUI
    id_num: int
    computed: bool

    def execute(self) -> Tuple[Any, ...]:
        """
        Compute the output values.
        The input values are guarenteed to be set correctly.
        Access them with ``self.inputs[x].value``
        Return the outputs as a tuple.
        The node tree will handle the rest.
        """
        raise NotImplementedError("The default implementation cannot be used.")


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

    def rm_connection(self, out_node_id: int, out_socket_num: int, in_node_id: int,
            in_socket_num: int) -> None:
        """
        Removes a connection between two nodes.

        :param out_node_id: Output node id.
        :param out_socket_num: Output node socket number.
        :param in_node_id: Input node id.
        :param in_socket_num: Input node socket number.
        """
        out_socket = self.get_node_by_id(out_node_id).outputs[out_socket_num]
        in_socket = self.get_node_by_id(in_node_id).inputs[in_socket_num]

        out_socket.connection = None
        in_socket.connection = None

    def _exe_inp(self, ind: int, socket_num: int) -> None:
        """
        Compute one input's value.

        :param ind: Node index, NOT the ID.
        :param socket_num: Input socket index.
        """
        inp = self.nodes[ind].inputs[socket_num]
        if inp.connection is None:
            inp.value = inp.gui_value
        else:
            node_id, num = inp.connection
            node = self.get_node_by_id(node_id)
            if not node.computed:
                self._exe_node(self.get_node_index_by_id(node_id))
            inp.set_value(node.outputs[num].value)
        inp.computed = True

    def _exe_node(self, ind: int) -> None:
        """
        Compute one node's value.

        :param ind: Node index, NOT the ID.
        """
        node = self.nodes[ind]
        for i, inp in enumerate(node.inputs):
            if not inp.computed:
                self._exe_inp(ind, i)

        values = node.execute()
        assert len(values) == len(node.outputs)
        for i, v in enumerate(values):
            node.outputs[i].set_value(v)

    def execute(self) -> None:
        """
        Computes each socket's value.
        """
        for node in self.nodes:
            node.computed = False
            for inp in node.inputs:
                inp.computed = False
            for out in node.outputs:
                out.computed = False

        for i, node in enumerate(self.nodes):
            if not node.computed:
                self._exe_node(i)
