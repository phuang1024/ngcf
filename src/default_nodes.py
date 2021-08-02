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

import ngcf
from ngcf import Node


class NodeLogicAnd(Node):
    inputs = (
        ngcf.SocketBool(name="A"),
        ngcf.SocketBool(name="B"),
    )
    outputs = (
        ngcf.SocketBool(name="Output"),
    )
    name = "AND"
    category = "Logic"

    def execute(self):
        return (self.get("A") and self.get("B"))

class NodeLogicOr(Node):
    inputs = (
        ngcf.SocketBool(name="A"),
        ngcf.SocketBool(name="B"),
    )
    outputs = (
        ngcf.SocketBool(name="Output"),
    )
    name = "OR"
    category = "Logic"

    def execute(self):
        return (self.get("A") or self.get("B"))

class NodeLogicXor(Node):
    inputs = (
        ngcf.SocketBool(name="A"),
        ngcf.SocketBool(name="B"),
    )
    outputs = (
        ngcf.SocketBool(name="Output"),
    )
    name = "XOR"
    category = "Logic"

    def execute(self):
        return (self.get("A") != self.get("B"))

class NodeLogicNot(Node):
    inputs = (
        ngcf.SocketBool(name="A"),
    )
    outputs = (
        ngcf.SocketBool(name="Output"),
    )
    name = "NOT"
    category = "Logic"

    def execute(self):
        return (not self.get("A"))


classes = (
    NodeLogicAnd,
    NodeLogicOr,
    NodeLogicXor,
    NodeLogicNot,
)

def register():
    for cls in classes:
        ngcf.register_node(cls)
