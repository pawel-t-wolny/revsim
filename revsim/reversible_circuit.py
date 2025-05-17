from bitarray import bitarray
from typing import List, Tuple

from .custom_types import Mapping, Registers
from .gates.not_gate import NotGate
from .gates.ccnot_gate import CCNotGate
from .gates.cnot_gate import CNotGate
from .reversible_gate import ReversibleGate
from .reversible_gate import Registers



class ReversibleCircuit:
    gates: List[Tuple[ReversibleGate, Mapping]]
    width: int

    def __init__(self, width: int, gates: List[ReversibleGate] = None):
        if gates is None:
            gates = []

        for gate in gates:
            assert gate.input_count <= width

        self.gates = gates
        self.width = width

    def run(self, initial_values: str) -> Registers:
        assert len(initial_values) == self.width
        registers = bitarray(initial_values)
        for gate, gate_mapping in self.gates:
            registers = gate.apply(registers, gate_mapping)

        return registers

    def assert_gate_and_mapping(self, gate: ReversibleGate, gate_mapping: Mapping):
        for i in gate_mapping:
            assert 0 <= i < self.width, f"Index {i} is invalid for the {gate.name} gate"

        assert (
            gate.input_count <= self.width
        ), f"The {gate.name} gate has more inputs than circuit registers"
        assert len(set(gate_mapping)) == len(
            gate_mapping
        ), f"There are non unique indexes in the gate mapping for '{gate.name}' gate"
        assert gate.input_count == len(
            gate_mapping
        ), f"The number of inputs is not equal to the number of indexes in gate mapping for '{gate.name}' gate"

    def append(self, gate: ReversibleGate, gate_mapping: Mapping):
        self.assert_gate_and_mapping(gate, gate_mapping)
        self.gates.append((gate, gate_mapping))

    def to_gate(self, name: str) -> ReversibleGate:
        from .gates.custom_gate import CustomGate

        return CustomGate(self, name)

    def x(self, target_bit: int):
        gate = NotGate()
        self.append(gate, [target_bit])

    def cx(self, control_bit: int, target_bit: int):
        gate = NotGate()
        self.append(gate, [control_bit, target_bit])

    def cx(self, control_bit: int, target_bit: int):
        gate = CNotGate()
        self.append(gate, [control_bit, target_bit])

    def ccx(self, control_bit1: int, control_bit2: int, target_bit: int):
        gate = CCNotGate()
        self.append(gate, [control_bit1, control_bit2, target_bit])
