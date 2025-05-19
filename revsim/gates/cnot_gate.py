from ..reversible_gate import ReversibleGate
from ..custom_types import Mapping, Registers


class CNotGate(ReversibleGate):

    def __init__(self):
        super().__init__(input_count=2, label="cnot")

    def apply(self, registers: Registers, gate_mapping: Mapping):
        self.assert_gate_mapping(registers, gate_mapping)

        control_bit = len(registers) - 1 - gate_mapping[0]
        target_bit = len(registers) - 1 - gate_mapping[1]

        if registers[control_bit] == 1:
            new_registers = registers.copy()
            new_registers[target_bit] ^= 1
            return new_registers
        return registers
