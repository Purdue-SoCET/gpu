# SoCET Cardinal GPU

## DOCUMENTATION IS A WORK IN PROGRESS
Please help with regular documentation where you can. When you create diagrams or set something in stone for the team, please document it here. This GitHub Page will serve as our source of truth for the GPU.

Feel free to restructure `docs/src` however needed to make your documentation make sense.

## Overview
SoCET in-house GPU implementation

SoCET Graphics Processing Unit team is split into three subteams: (1) hardware team, (2) compilers team, and (3) graphics workflow. 

## projects
### Emulator
The emulator is a functional simulator that simulates the architectural correctness of the hardware. It can help validate software and compiler's effort, as well as provide expected output for the cycle-accurate simulator or RTL.

### funcsim
funcsim is a cycle-accurate simulator that details the microarchitecture of the GPU.
Performance counters should also be included to study the bottleneck of the design. 