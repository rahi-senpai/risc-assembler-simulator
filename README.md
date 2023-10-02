# SimpleRISC Assembler and Simulator
Starter repository for the course CSE112 - Computer Organisation (Winter 2023), IIIT Delhi.
Here's an assembler and a simulator based on SimpleRISC ISA implemented in Python, along with automated testing routines.

## Instructions
The assembler code is in `Simple-Assembler/assembler.py`.
The simulator code is in `SimpleSimulator/simulator.py`.
The assembler and simulator reads from `stdin` and writes to `stdout`.

To evaluate, go to the `automatedTesting` directory in your terminal and execute `./run` with none or appropriate arguments:
`--no-sim`: to only evaluate assembler
`--no-asm`: to only evaluate simulator

(If you are interested, test2 and test3 in simulator hard tests have less memory dump than specified, i.e.128, and hence they are wrong (add the required lines of 0s to correct them), sort of _booby traps_.)

## Collaborators
Himanshu Raj [@rahi-senpai](https://www.github.com/rahi-senpai)
Aayush Mishra [@alexaplsburp](https://www.github.com/alexaplsburp)
Dhruv Prakash [@14dhruv04](https://www.github.com/14dhruv04)
Kirti Jain [@kiwiikirtii](https://www.github.com/kiwiikirtii)