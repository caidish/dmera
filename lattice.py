# This is part of the DMERA project(https://github.com/ikim-quantum/dmera).
# Copyright (C) 2018 Isaac H. Kim.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import numpy as np
from qubit import Qubit


class Point(tuple):
    """
    Points on a square lattice
    """
    def __init__(self, v):
        self = tuple(v)
        return self

    def __mul__(self, other):
        if isinstance(other, int):
            return Point([n * other for n in self])
        elif isinstance(other, tuple):
            return Point([n * factor for n, factor in zip(self, other)])

    def __imul__(self, other):
        self = self * other
        return self

    def __add__(self, other):
        return Point([i + j for i, j in zip(self, other)])

    def __iadd__(self, other):
        self = self + other
        return self

    def __sub__(self, other):
        return Point([i - j for i, j in zip(self, other)])

    def __isub__(self, other):
        self = self - other
        return self


class Lattice():
    def __init__(self, size=1):
        """
        Generates a lattice of size l_1 x l_2 x ... for size = (l_1, l_2,
        ...). Each lattice site contains a qubit.

        Args:
            size(list of int): length of the lattice in each directions
        """
        self.pts = [Point(loc) for loc in np.ndindex(tuple(size))]
        self.qubits = {v: Qubit(v) for v in self.pts}
        self.d = dim_spatial(size)
        self.size = Point(size)

    def fine_grain(self, blowup_factor):
        """
        Fine-grain the existing lattice into a larger lattice
        """
        if isinstance(blowup_factor, int):
            factor = tuple([blowup_factor for i in range(self.d)])
        else:
            factor = tuple(blowup_factor)
        self.size *= factor
        # set of new points
        pts = [Point(loc) for loc in np.ndindex(self.size)]
        pts_inherited = [v * factor for v in self.pts]
        pts_new = [loc for loc in pts if loc not in pts_inherited]

        # embed the old qubits to a new lattice
        self.qubits = {v * factor: self.qubits[v] for v in self.pts}
        # change the label_circuit for the old qubits
        for v in pts_inherited:
            self.qubits[v].label_circuit = v
        # introduce the new qubits
        for v in pts_new:
            self.qubits[v] = Qubit(v)
        # update the set of points
        self.pts = pts


def dim_spatial(size):
    if isinstance(size, int):
        return 1
    elif isinstance(size, list):
        for n in size:
            if not isinstance(n, int):
                raise TypeError("The size should be specified as integers.")
            elif n < 1:
                return ValueError("Integer is not positive.")
        return len(size)
    else:
        raise TypeError("Input should be an integer or a list of integers.")
