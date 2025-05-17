from ..reversible_gate import ReversibleGate
from ..custom_types import Mapping, Registers


class NotGate(ReversibleGate):

    def __init__(self):
        super().__init__(input_count=1, name="not")

    def apply(self, registers: Registers, gate_mapping: Mapping):
        self.assert_gate_mapping(registers, gate_mapping)

        new_registers = registers.copy()
        target_bit = len(registers) - 1 - gate_mapping[0]
        new_registers[target_bit] ^= 1

        return new_registers
