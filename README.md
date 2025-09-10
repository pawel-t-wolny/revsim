# revsim

A Python library for simulating reversible circuits classically. Built this for my [bachelor thesis](https://www.cs.ru.nl/bachelors-theses/2025/Pawe%C5%82_Wolny___1092613___Design_and_Optimization_of_a_Grover's_Oracle_for_Quantum_Preimage_Attacks_on_SPONGENT_Hash_Function.pdf) to validate quantum implementations of the SPONGENT hash function against the reference C implemetation.

## Installation

```bash
pip install git+https://github.com/pawel-t-wolny/revsim.git
```

## Usage

```python
from revsim import ReversibleCircuit

# Create a 3-bit circuit
circuit = ReversibleCircuit(width=3)

# Add some gates
circuit.x(0)           # NOT gate on bit 0
circuit.cx(1, 2)       # CNOT: control=1, target=2  
circuit.ccx(0, 1, 2)   # Toffoli gate

# Run with initial state "001"
result = circuit.run("001")
print(result)  # outputs the final bitarray
```

## What it does

This simulator lets you build and run reversible logic circuits using basic gates:
- `x(target)` - NOT gate (bit flip)
- `cx(control, target)` - CNOT gate 
- `ccx(control1, control2, target)` - Toffoli gate

You can also create custom gates from existing circuits:

```python
# Build a subcircuit
sub = ReversibleCircuit(width=2)
sub.x(0)
sub.cx(0, 1)

# Turn it into a reusable gate
custom_gate = sub.to_gate("my_gate")

# Use it in a bigger circuit
main = ReversibleCircuit(width=4)
main.append(custom_gate, [0, 1])  # apply to bits 0,1
```

## Why I built this

I needed to verify that my quantum implementation of SPONGENT was correct by testing it against a reference implementation for a bunch of different inputs. However, doing a proper quantum simulation - even on the smallest instance of SPONGENT - was impossible. This is due to the complex and expensive nature of quantum circuit simulation. However, using the fact that the circuit itself was built only using NOT, CNOT, and Toffoli (CCNOT) gates, meant that for the purpouse of verifying correctness, we can ignore away the quantum effects and simulate it classically. However, Qiskit did not seem to have a classical simulator. So I implemented my own which closely follows the notations used in Qiskit, so that it is easy to transition between one and the other.

The implementation uses bitarrays for efficiency since all the gates in the circuit are simply bit manipulations.

## Structure

- `ReversibleCircuit` - main class for building circuits
- `ReversibleGate` - abstract base for all gates  
- `gates/` - implementations of NOT, CNOT, Toffoli gates
- `CustomGate` - lets you turn circuits into reusable components

## Requirements

- Python 3.8+
- bitarray
