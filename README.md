# SimpleRISC Assembler and Simulator
Starter repository for the course CSE112 - Computer Organisation (Winter 2023), IIIT Delhi.<br />
Here's an assembler and a simulator based on SimpleRISC ISA implemented in Python, along with automated testing routines.

## Instructions
The assembler code is in `Simple-Assembler/assembler.py`.<br />
The simulator code is in `SimpleSimulator/simulator.py`.<br />
The assembler and simulator reads from `stdin` and writes to `stdout`.<br />

To evaluate, go to the `automatedTesting` directory in your terminal and execute `./run` with none or appropriate arguments:<br />
`--no-sim`: to only evaluate assembler<br />
`--no-asm`: to only evaluate simulator<br />

(If you are interested, test2 and test3 in simulator hard tests have less memory dump than specified, i.e.128 and hence they are wrong (add the required lines of 0s to correct them), sort of _booby traps_.)

## Collaborators
Aayush Mishra [@alexaplsburp](https://www.github.com/alexaplsburp)<br />
Dhruv Prakash [@14dhruv04](https://www.github.com/14dhruv04)<br />
Himanshu Raj [@rahi-senpai](https://www.github.com/rahi-senpai)<br />
Kirti Jain [@kiwiikirtii](https://www.github.com/kiwiikirtii)
