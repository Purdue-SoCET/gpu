       section data
       global cos
       type cos func
       global sin
       type sin func
       global ftoi
       type ftoi func
       global itof
       type itof func
       global isqrt
       type isqrt func
       global blockIdx
       type blockIdx func
       global blockDim
       type blockDim func
       global threadIdx
       type threadIdx func
       section data
       section code
       global kernel_add
       type kernel_add func
 kernel_add:
       lui, x11, 255
       lmi, x11, 4095
       lli, x11, 2672
       add x2, x2, x11
       lui, x11, 0
       lmi, x11, 0
       lli, x11, 128
       add x11, x2, x11
       sw x1, 0(x11)
       sw x8, 0(x2)
       lui, x11, 0
       lmi, x11, 0
       lli, x11, 256
       add x8, x2, x11
       sw x9, 0(x8)
 kernel_add_block0:
       jal x0, kernel_add_block1
 kernel_add_block1:
       lui, x11, 0
       lmi, x11, 0
       lli, x11, 512
       add x11, x8, x11
       sw x12, 0(x11)
       lui, x11, 0
       lmi, x11, 0
       lli, x11, 512
       add x11, x8, x11
       lw x9, 0(x11)
       lui, x11, 0
       lmi, x11, 0
       lli, x11, 384
       add x11, x8, x11
       sw x9, 0(x11)
       csrr x11, 2
       csrr x10, 3
       csrr x9, 1
       mul x10, x11, x10
       add x9, x10, x9
       lui, x11, 0
       lmi, x11, 0
       lli, x11, 256
       add x11, x8, x11
       sw x9, 0(x11)
       lui, x11, 0
       lmi, x11, 0
       lli, x11, 384
       add x11, x8, x11
       lw x9, 0(x11)
       addi x9, x9, 8
       lw x13, 0(x9)
       lui, x11, 0
       lmi, x11, 0
       lli, x11, 256
       add x11, x8, x11
       lw x12, 0(x11)
       lui, x11, 0
       lmi, x11, 0
       lli, x11, 384
       add x11, x8, x11
       lw x9, 0(x11)
       addi x9, x9, 0
       lw x10, 0(x9)
       lui, x11, 0
       lmi, x11, 0
       lli, x11, 256
       add x11, x8, x11
       lw x9, 0(x11)
       addi x11, x0, 4
       mul x9, x9, x11
       add x9, x10, x9
       lw x11, 0(x9)
       lui, x11, 0
       lmi, x11, 0
       lli, x11, 384
       add x11, x8, x11
       lw x9, 0(x11)
       addi x9, x9, 4
       lw x10, 0(x9)
       lui, x11, 0
       lmi, x11, 0
       lli, x11, 256
       add x11, x8, x11
       lw x9, 0(x11)
       addi x14, x0, 4
       mul x9, x9, x14
       add x9, x10, x9
       lw x9, 0(x9)
       addi x10, x0, 4
       mul x10, x12, x10
       add x10, x13, x10
       add x9, x11, x9
       sw x9, 0(x10)
       jal x0, kernel_add_epilog
 kernel_add_epilog:
       lw x9, 0(x8)
       lui, x11, 0
       lmi, x11, 0
       lli, x11, 128
       add x11, x2, x11
       lw x1, 0(x11)
       lw x8, 0(x2)
       lui, x11, 0
       lmi, x11, 0
       lli, x11, 1424
       add x2, x2, x11
       jalr x0,x1, 0
       .align 4
