from ..reversible_gate import ReversibleGate
from ..reversible_circuit import ReversibleCircuit
from ..custom_types import Mapping, Registers


class CustomGate(ReversibleGate):
    circuit: ReversibleCircuit
    name: str

    def __init__(self, circuit: ReversibleCircuit, name: str):
        super().__init__(input_count=circuit.width, name=name)
        self.circuit = circuit

    def apply(self, registers: Registers, gate_mapping: Mapping):
        new_registers = registers.copy()
        input_values = [registers[-1 - bit] for bit in reversed(gate_mapping)]

        output = self.circuit.run(input_values)

        for index, output_bit in zip(reversed(gate_mapping), output):
            new_registers[-1 - index] = output_bit

        return new_registers
