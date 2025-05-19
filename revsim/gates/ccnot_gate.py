from ..reversible_gate import ReversibleGate
from ..custom_types import Mapping, Registers


class CCNotGate(ReversibleGate):

    def __init__(self):
        super().__init__(input_count=3, label="ccnot")

    def apply(self, registers: Registers, gate_mapping: Mapping):
        self.assert_gate_mapping(registers, gate_mapping)

        first_control_bit = len(registers) - 1 - gate_mapping[0]
        second_control_bit = len(registers) - 1 - gate_mapping[1]
        target_bit = len(registers) - 1 - gate_mapping[2]

        if registers[first_control_bit] == 1 and registers[second_control_bit] == 1:
            new_registers = registers.copy()
            new_registers[target_bit] ^= 1
            return new_registers
        return registers
