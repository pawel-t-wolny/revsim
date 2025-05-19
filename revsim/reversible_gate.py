from abc import ABC, abstractmethod
from .custom_types import Mapping, Registers


class ReversibleGate(ABC):

    #   Gate mapping determines mapping of gate inputs to the input registers.
    #   The drawing below shows how would the input bits be mapped when gate_mapping = [0,1,2].
    #
    #         Inputs:    X3     X2     X1     X0
    #                     |      |      |      |
    #                     |      v      v      v
    #                     |    +-----------------+
    #                     |    | 2      1      0 |
    #                     |    |    3x3 Gate     |
    #                     |    |                 |
    #                     |    +-----------------+
    #                     |      |      |      |
    #         Outputs:   Y0     Y1     Y2     Y3
    #
    #   If gate_mapping = [3, 0, 1], the circuit will look as follows:
    #
    #         Inputs:    X3     X2     X1     X0
    #                     |      |      |      |
    #                     v      |      v      v
    #                 +--------------------------+
    #                 |   0             2      1 |
    #                 |      Custom 3x3 Gate     |
    #                 |                          |
    #                 +--------------------------+
    #                     |      |      |      |
    #         Outputs:   Y0     Y1     Y2     Y3
    #
    #   So for each entry of the array think like "The input 0 of the gate gets mapped to input register 3,
    #   input 1 gets mapped to input register 0, etc.".
    #
    #   To make it even more cleare here is a more explict example with a CCNOT gate on 4 registers. When
    #   gate_mapping = [0, 1, 2] we get:
    #
    #         Inputs:    X3     X2     X1     X0
    #                     |      |      |      |
    #                     v      v      v      v
    #                     |      2      1      0
    #                     |      X------o------o
    #                     |      |      |      |
    #         Outputs:   Y0     Y1     Y2     Y3
    #
    #   Let's say we want to remap the gate using gate_mapping = [3, 0, 1]. Then we get:
    #
    #         Inputs:    X3     X2     X1     X0
    #                     |      |      |      |
    #                     v      v      v      v
    #                     0      |      2      1
    #                     o-------------X------o
    #                     |      |      |      |
    #         Outputs:   Y0     Y1     Y2     Y3
    #
    #   As we can see, the input 0 of the CNOT gate was mapped to input register X3,
    #   input 1 of the CNOT gate to input register X0 and input 2 of the CNOT gate was
    #   mapped to input register X1.

    input_count: int
    label: str

    def __init__(self, input_count: int, label: str):
        super().__init__()

        self.input_count = input_count
        self.label = label

    def assert_gate_mapping(self, registers: Registers, gate_mapping: Mapping):
        for i in gate_mapping:
            assert (
                0 <= i < len(registers)
            ), f"Some indexes in the gate mapping do not correspond to registers for '{self.label}' gate"

        assert len(set(gate_mapping)) == len(
            gate_mapping
        ), f"There are non unique indexes in the gate mapping for '{self.label}' gate"

        assert self.input_count == len(
            gate_mapping
        ), f"The number of inputs is not equal to the number of indexes in gate mapping for '{self.label}' gate"

    @abstractmethod
    def apply(self, registers: Registers, gate_mapping: Mapping) -> Registers: ...
