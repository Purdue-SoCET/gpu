import sys
from pathlib import Path
from reg_file import * 
from instr import *
from warp import *
from mem import *
from custom_enums import *
# print csr helper
def print_csr(csr):
    for i in range(len(csr["x"])):
        print(f"lane {i:2d}: (z={csr['z'][i]}, y={csr['y'][i]}, x={csr['x'][i]})")


# thread block scheduler
def tbs(x, y, z):
    blocksize = x*y*z

    if blocksize > 32:
        print("fuck you 3")
        sys.exit(1)

    csr = {"x": [i % x for i in range(blocksize)], "y": [(i // x) % y for i in range(blocksize)], "z": [i // (x * y) for i in range(blocksize)]}
    return csr

# actual emulator
def emulator(csr, regfile, input_file, mem):
    with open(input_file, "r") as f:
        instructions = f.readlines()

    ### STARTING PC IS ASSUMED ZERO FOR NOW BUT UPDATE IT ACCORDING TO WHAT SOFTWARE GIVES US
    pc = 0
    halt = False

    while not halt and pc < len(instructions):
        line = instructions[pc].strip()

        #compiler is big endian:MSB at smallest addr
        instr_type = Bits(bin=line[28:32], length=4) # bits 31:28
        funct = Bits(bin=line[25:28], length=3) # bits 27:25

        match Instr_Type(instr_type):
            case Instr_Type.R_TYPE_0:
                op = R_Op_0(funct)
                rs2 = Bits(bin=line[8:13]) #12:8
                rs1 = Bits(bin=line[13:19]) #18:13
                rd = Bits(bin=line[19:25]) #24:19
                instr = R_Instr_0(op=op, rs1=rs1, rs2=rs2, rd=rd)
                print("rtype_0")  
            case Instr_Type.R_TYPE_1:
                op = R_Op_1(funct)
                rs2 = Bits(bin=line[8:13]) #12:8
                rs1 = Bits(bin=line[13:19]) #18:13
                rd = Bits(bin=line[19:25]) #24:19
                instr = R_Instr_1(op=op, rs1=rs1, rs2=rs2, rd=rd)
                print("rtype_1")  
            case Instr_Type.I_TYPE_0:
                print("itype_0")
            case Instr_Type.I_TYPE_1:
                print("itype_1")
            case Instr_Type.I_TYPE_2:
                print("itype_2")
            case Instr_Type.S_TYPE_0:
                print("stype_0")
            case Instr_Type.S_TYPE_1:
                print("stype_1")
            case Instr_Type.B_TYPE_0:
                print("btype")
            case Instr_Type.B_TYPE_1:
                print("btype")
            case Instr_Type.U_TYPE:
                print("utype")
            case Instr_Type.J_TYPE:
                print("jtype")
            case Instr_Type.P_TYPE:
                print("ptype")
            case Instr_Type.C_TYPE:
                print("ctype")
            case _:
                print("Undefined opcode")
                
    return

# main function
if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("fuck u lol")
        sys.exit(1)

    input_file = Path(sys.argv[1])

    if not input_file.exists():
        print("fuck u again lol")
        sys.exit(1)

    csr = tbs(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
    warp = Warp(0)
    emulator(csr, warp.reg_files, sys.argv[1], "e")
    # regfile = [[0 for i in range(32)] for j in range(32)]

    # print_csr(csr) # uncomment to print out csr
