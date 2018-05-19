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

from circuit import Circuit
from lattice import Lattice

class DMERA1(Circuit):
    """
    This is a DMERA circuit ansatz for quantum many-body systems in
    one spatial dimension.
    """

    def __init__(self, scales=0, depth=0):
        """
        Initializes the instance with a DMERA with identity gates.

        Args:
            scales (int): Number of qubits = 2 ** scales
            depth (int): Depth per scale
        """
        unitsize = 2 * depth
        self.lattices = [Lattice(unitsize)]
        for scale in range(1, scales):
            self.lattices.append(self.lattices[-1].expand(2))
        



class Slice(circuit):
    """
    Single-depth quantum circuit. Translationally invariant. Specified by
    a single two-qubit gate.
    """

    def __init__(self, my_lattice):
        if not isinstance(my_lattice, Lattice):
            raise TypeError("Input for LDQC __init__ must be a Lattice.")
