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
    "Socket",
    "SocketBool",
    "SocketInt",
    "SocketFloat",
    "SocketStr",
)

from typing import Any, Tuple, Union


class Socket:
    """Base node socket."""
    name: str
    default: Any

    # Updated by the node tree and/or GUI
    value: Any
    gui_value: Any
    computed: bool
    connection: Union[None, Tuple[int, int]]

    def __init__(self):
        """
        Call ``super().__init__()`` AFTER setting ``self.default``
        """
        self.connection = None
        self.value = self.default
        self.gui_value = self.default

    def set_value(self, value: Any) -> None:
        self.value = value
        self.gui_value = value


class SocketBool(Socket):
    """Boolean socket."""

    def __init__(self, name: str = "", default: bool = False) -> None:
        self.name = name
        self.default = default
        super().__init__()


class SocketInt(Socket):
    """Integer socket."""

    min: int
    max: int

    def __init__(self, name: str = "", default: int = 0, min: int = int(-1e9), max: int = int(1e9)) -> None:
        self.name = name
        self.default = default
        self.min = min
        self.max = max
        super().__init__()

    def set_value(self, value: int) -> None:
        self.value = max(min(value, self.max), self.min)


class SocketFloat(Socket):
    """Float64 socket."""

    min: float
    max: float

    def __init__(self, name: str = "", default: float = 0, min: float = -1e9, max: float = 1e9) -> None:
        self.name = name
        self.default = default
        self.min = min
        self.max = max
        super().__init__()

    def set_value(self, value: float) -> None:
        self.value = max(min(value, self.max), self.min)


class SocketStr(Socket):
    """String socket."""

    max_len: int

    def __init__(self, name: str = "", default: float = 0, max_len: int = int(1e4)) -> None:
        self.name = name
        self.default = default
        self.max_len = max_len
        super().__init__()

    def set_value(self, value: str) -> None:
        self.value = value[:self.max_len]
