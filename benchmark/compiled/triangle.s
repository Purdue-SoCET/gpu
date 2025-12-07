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
       global kernel_triangle
       type kernel_triangle func
 kernel_triangle:
       lui, x11, 255
       lmi, x11, 4095
       lli, x11, 1008
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
       lui, x11, 0
       lmi, x11, 0
       lli, x11, 128
       add x11, x8, x11
       sw x18, 0(x11)
 kernel_triangle_block0:
       jal x0, kernel_triangle_block1
 kernel_triangle_block1:
       lui, x11, 0
       lmi, x11, 0
       lli, x11, 2176
       add x11, x8, x11
       sw x12, 0(x11)
       lui, x11, 0
       lmi, x11, 0
       lli, x11, 2176
       add x11, x8, x11
       lw x9, 0(x11)
       lui, x11, 0
       lmi, x11, 0
       lli, x11, 2048
       add x11, x8, x11
       sw x9, 0(x11)
       addi x9, x0, 0
       lui, x11, 0
       lmi, x11, 0
       lli, x11, 1920
       add x11, x8, x11
       sw x9, 0(x11)
       addi x9, x0, 0
       lui, x11, 0
       lmi, x11, 0
       lli, x11, 1792
       add x11, x8, x11
       sw x9, 0(x11)
       lui, x11, 0
       lmi, x11, 0
       lli, x11, 1920
       add x11, x8, x11
       lw x11, 0(x11)
       lui, x11, 0
       lmi, x11, 0
       lli, x11, 2048
       add x11, x8, x11
       lw x9, 0(x11)
       addi x13, x9, 0
       addi x12, x0, 0
       addi x9, x0, 4
       mul x9, x12, x9
       add x9, x13, x9
       lw x9, 0(x9)
       add x9, x11, x9
       lui, x11, 0
       lmi, x11, 0
       lli, x11, 1664
       add x11, x8, x11
       sw x9, 0(x11)
       lui, x11, 0
       lmi, x11, 0
       lli, x11, 1792
       add x11, x8, x11
       lw x11, 0(x11)
       lui, x11, 0
       lmi, x11, 0
       lli, x11, 2048
       add x11, x8, x11
       lw x9, 0(x11)
       addi x13, x9, 0
       addi x12, x0, 1
       addi x9, x0, 4
       mul x9, x12, x9
       add x9, x13, x9
       lw x9, 0(x9)
       add x9, x11, x9
       lui, x11, 0
       lmi, x11, 0
       lli, x11, 1536
       add x11, x8, x11
       sw x9, 0(x11)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 4060
       add x12, x8, x9
       addi x11, x0, 0
       addi x9, x0, 4
       mul x9, x11, x9
       add x11, x12, x9
       lui, x9, 63
       lmi, x9, 2048
       lli, x9, 0
       sw x9, 0(x11)
       lui, x11, 0
       lmi, x11, 0
       lli, x11, 1664
       add x11, x8, x11
       lw x9, 0(x11)
       lui, x11, 255
       lmi, x11, 4095
       lli, x11, 4060
       add x13, x8, x11
       addi x12, x0, 1
       addi x11, x0, 4
       mul x11, x12, x11
       add x12, x13, x11
       itof x11, x9
       lui, x9, 63
       lmi, x9, 0
       lli, x9, 0
       addf x9, x11, x9
       sw x9, 0(x12)
       lui, x11, 0
       lmi, x11, 0
       lli, x11, 1536
       add x11, x8, x11
       lw x9, 0(x11)
       lui, x11, 255
       lmi, x11, 4095
       lli, x11, 4060
       add x13, x8, x11
       addi x12, x0, 2
       addi x11, x0, 4
       mul x11, x12, x11
       add x12, x13, x11
       itof x11, x9
       lui, x9, 63
       lmi, x9, 0
       lli, x9, 0
       addf x9, x11, x9
       sw x9, 0(x12)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 4060
       add x12, x8, x9
       addi x11, x0, 0
       addi x9, x0, 4
       mul x9, x11, x9
       add x9, x12, x9
       lw x15, 0(x9)
       lui, x11, 0
       lmi, x11, 0
       lli, x11, 2048
       add x11, x8, x11
       lw x9, 0(x11)
       addi x12, x9, 16
       addi x11, x0, 0
       addi x9, x0, 12
       mul x9, x11, x9
       add x12, x12, x9
       addi x11, x0, 0
       addi x9, x0, 4
       mul x9, x11, x9
       add x9, x12, x9
       lw x14, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 4060
       add x12, x8, x9
       addi x11, x0, 1
       addi x9, x0, 4
       mul x9, x11, x9
       add x9, x12, x9
       lw x13, 0(x9)
       lui, x11, 0
       lmi, x11, 0
       lli, x11, 2048
       add x11, x8, x11
       lw x9, 0(x11)
       addi x12, x9, 16
       addi x11, x0, 0
       addi x9, x0, 12
       mul x9, x11, x9
       add x12, x12, x9
       addi x11, x0, 1
       addi x9, x0, 4
       mul x9, x11, x9
       add x9, x12, x9
       lw x12, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 4060
       add x16, x8, x9
       addi x11, x0, 2
       addi x9, x0, 4
       mul x9, x11, x9
       add x9, x16, x9
       lw x11, 0(x9)
       lui, x11, 0
       lmi, x11, 0
       lli, x11, 2048
       add x11, x8, x11
       lw x9, 0(x11)
       addi x17, x9, 16
       addi x16, x0, 0
       addi x9, x0, 12
       mul x9, x16, x9
       add x17, x17, x9
       addi x16, x0, 2
       addi x9, x0, 4
       mul x9, x16, x9
       add x9, x17, x9
       lw x9, 0(x9)
       lui, x16, 255
       lmi, x16, 4095
       lli, x16, 4048
       add x16, x8, x16
       mulf x14, x15, x14
       mulf x12, x13, x12
       addf x12, x14, x12
       mulf x9, x11, x9
       addf x9, x12, x9
       sw x9, 0(x16)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 4060
       add x12, x8, x9
       addi x11, x0, 0
       addi x9, x0, 4
       mul x9, x11, x9
       add x9, x12, x9
       lw x15, 0(x9)
       lui, x11, 0
       lmi, x11, 0
       lli, x11, 2048
       add x11, x8, x11
       lw x9, 0(x11)
       addi x12, x9, 16
       addi x11, x0, 1
       addi x9, x0, 12
       mul x9, x11, x9
       add x12, x12, x9
       addi x11, x0, 0
       addi x9, x0, 4
       mul x9, x11, x9
       add x9, x12, x9
       lw x14, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 4060
       add x12, x8, x9
       addi x11, x0, 1
       addi x9, x0, 4
       mul x9, x11, x9
       add x9, x12, x9
       lw x13, 0(x9)
       lui, x11, 0
       lmi, x11, 0
       lli, x11, 2048
       add x11, x8, x11
       lw x9, 0(x11)
       addi x12, x9, 16
       addi x11, x0, 1
       addi x9, x0, 12
       mul x9, x11, x9
       add x12, x12, x9
       addi x11, x0, 1
       addi x9, x0, 4
       mul x9, x11, x9
       add x9, x12, x9
       lw x11, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 4060
       add x16, x8, x9
       addi x12, x0, 2
       addi x9, x0, 4
       mul x9, x12, x9
       add x9, x16, x9
       lw x12, 0(x9)
       lui, x11, 0
       lmi, x11, 0
       lli, x11, 2048
       add x11, x8, x11
       lw x9, 0(x11)
       lui, x16, 255
       lmi, x16, 4095
       lli, x16, 4048
       add x16, x8, x16
       addi x17, x16, 4
       mulf x14, x15, x14
       mulf x11, x13, x11
       addf x11, x14, x11
       addi x14, x9, 16
       addi x13, x0, 1
       addi x9, x0, 12
       mul x9, x13, x9
       add x9, x14, x9
       jal x0, kernel_triangle_splitted_block_1
 kernel_triangle_block2:
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 4048
       add x11, x8, x9
       addi x10, x0, 0
       addi x9, x0, 4
       mul x9, x10, x9
       add x9, x11, x9
       lw x14, 0(x9)
       lui, x11, 0
       lmi, x11, 0
       lli, x11, 2048
       add x11, x8, x11
       lw x9, 0(x11)
       lui, x10, 0
       lmi, x10, 0
       lli, x10, 56
       add x11, x9, x10
       addi x10, x0, 0
       addi x9, x0, 12
       mul x9, x10, x9
       add x9, x11, x9
       addi x9, x9, 8
       lw x13, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 4048
       add x11, x8, x9
       addi x10, x0, 1
       addi x9, x0, 4
       mul x9, x10, x9
       add x9, x11, x9
       lw x12, 0(x9)
       lui, x11, 0
       lmi, x11, 0
       lli, x11, 2048
       add x11, x8, x11
       lw x9, 0(x11)
       lui, x10, 0
       lmi, x10, 0
       lli, x10, 56
       add x11, x9, x10
       addi x10, x0, 1
       addi x9, x0, 12
       mul x9, x10, x9
       add x9, x11, x9
       addi x9, x9, 8
       lw x11, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 4048
       add x15, x8, x9
       addi x10, x0, 2
       addi x9, x0, 4
       mul x9, x10, x9
       add x9, x15, x9
       lw x10, 0(x9)
       lui, x11, 0
       lmi, x11, 0
       lli, x11, 2048
       add x11, x8, x11
       lw x9, 0(x11)
       lui, x15, 0
       lmi, x15, 0
       lli, x15, 56
       add x16, x9, x15
       addi x15, x0, 2
       addi x9, x0, 12
       mul x9, x15, x9
       add x9, x16, x9
       addi x9, x9, 8
       lw x9, 0(x9)
       lui, x15, 255
       lmi, x15, 4095
       lli, x15, 4044
       add x15, x8, x15
       mulf x13, x14, x13
       mulf x11, x12, x11
       addf x11, x13, x11
       mulf x9, x10, x9
       addf x9, x11, x9
       sw x9, 0(x15)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 4044
       add x9, x8, x9
       lw x13, 0(x9)
       lui, x11, 0
       lmi, x11, 0
       lli, x11, 2048
       add x11, x8, x11
       lw x9, 0(x11)
       lui, x10, 0
       lmi, x10, 0
       lli, x10, 100
       add x9, x9, x10
       lw x12, 0(x9)
       lui, x11, 0
       lmi, x11, 0
       lli, x11, 1536
       add x11, x8, x11
       lw x11, 0(x11)
       lui, x11, 0
       lmi, x11, 0
       lli, x11, 2048
       add x11, x8, x11
       lw x9, 0(x11)
       lui, x10, 0
       lmi, x10, 0
       lli, x10, 92
       add x9, x9, x10
       lw x10, 0(x9)
       lui, x11, 0
       lmi, x11, 0
       lli, x11, 1664
       add x11, x8, x11
       lw x9, 0(x11)
       mul x10, x11, x10
       add x10, x10, x9
       addi x9, x0, 4
       mul x9, x10, x9
       add x9, x12, x9
       lw x9, 0(x9)
       bltf 7, x13, x9, 0
       bgef 8, x13, x9, 0
       jal x0, kernel_triangle_block18
 kernel_triangle_block3:
       jal x0, kernel_triangle_epilog
 kernel_triangle_block4:
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 4048
       add x12, x8, x9
       addi x11, x0, 1
       addi x9, x0, 4
       mul x9, x11, x9
       add x9, x12, x9
       lw x9, 0(x9)
       lui, x12, 55
       lmi, x12, 636
       lli, x12, 1452
       global float32_neg
       jal x1, float32_neg
       bltf 3, x9, x10, 0
       bgef 4, x9, x10, 0
       jal x0, kernel_triangle_block7
 kernel_triangle_block6:
       jal x0, kernel_triangle_block2
 kernel_triangle_block7:
       jal x0, kernel_triangle_epilog
 kernel_triangle_block8:
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 4048
       add x12, x8, x9
       addi x11, x0, 2
       addi x9, x0, 4
       mul x9, x11, x9
       add x9, x12, x9
       lw x9, 0(x9)
       lui, x12, 55
       lmi, x12, 636
       lli, x12, 1452
       global float32_neg
       jal x1, float32_neg
       bltf 5, x9, x10, 0
       bgef 6, x9, x10, 0
       jal x0, kernel_triangle_block11
 kernel_triangle_block10:
       jal x0, kernel_triangle_block6
 kernel_triangle_block11:
       jal x0, kernel_triangle_epilog
 kernel_triangle_block12:
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 4048
       add x11, x8, x9
       addi x10, x0, 0
       addi x9, x0, 4
       mul x9, x10, x9
       add x9, x11, x9
       lw x11, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 4048
       add x12, x8, x9
       addi x10, x0, 1
       addi x9, x0, 4
       mul x9, x10, x9
       add x9, x12, x9
       lw x10, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 4048
       add x13, x8, x9
       addi x12, x0, 2
       addi x9, x0, 4
       mul x9, x12, x9
       add x9, x13, x9
       lw x9, 0(x9)
       addf x10, x11, x10
       addf x10, x10, x9
       lui, x9, 63
       lmi, x9, 2068
       lli, x9, 1966
       bltf 7, x9, x10, 0
       bgef 8, x9, x10, 0
       jal x0, kernel_triangle_block15
 kernel_triangle_block14:
       jal x0, kernel_triangle_block10
 kernel_triangle_block15:
       jal x0, kernel_triangle_epilog
 kernel_triangle_block17:
       lui, x11, 0
       lmi, x11, 0
       lli, x11, 2048
       add x11, x8, x11
       lw x9, 0(x11)
       lui, x10, 0
       lmi, x10, 0
       lli, x10, 100
       add x9, x9, x10
       lw x13, 0(x9)
       lui, x11, 0
       lmi, x11, 0
       lli, x11, 1536
       add x11, x8, x11
       lw x12, 0(x11)
       lui, x11, 0
       lmi, x11, 0
       lli, x11, 2048
       add x11, x8, x11
       lw x9, 0(x11)
       lui, x10, 0
       lmi, x10, 0
       lli, x10, 92
       add x9, x9, x10
       lw x11, 0(x9)
       lui, x11, 0
       lmi, x11, 0
       lli, x11, 1664
       add x11, x8, x11
       lw x10, 0(x11)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 4044
       add x9, x8, x9
       lw x9, 0(x9)
       mul x11, x12, x11
       add x11, x11, x10
       addi x10, x0, 4
       mul x10, x11, x10
       add x10, x13, x10
       sw x9, 0(x10)
       lui, x11, 0
       lmi, x11, 0
       lli, x11, 2048
       add x11, x8, x11
       lw x9, 0(x11)
       lui, x10, 0
       lmi, x10, 0
       lli, x10, 104
       add x9, x9, x10
       lw x13, 0(x9)
       lui, x11, 0
       lmi, x11, 0
       lli, x11, 1536
       add x11, x8, x11
       lw x12, 0(x11)
       lui, x11, 0
       lmi, x11, 0
       lli, x11, 2048
       add x11, x8, x11
       lw x9, 0(x11)
       lui, x10, 0
       lmi, x10, 0
       lli, x10, 92
       add x9, x9, x10
       lw x11, 0(x9)
       lui, x11, 0
       lmi, x11, 0
       lli, x11, 1664
       add x11, x8, x11
       lw x10, 0(x11)
       lui, x11, 0
       lmi, x11, 0
       lli, x11, 2048
       add x11, x8, x11
       lw x9, 0(x11)
       lui, x14, 0
       lmi, x14, 0
       lli, x14, 52
       add x9, x9, x14
       lw x9, 0(x9)
       mul x11, x12, x11
       add x11, x11, x10
       addi x10, x0, 4
       mul x10, x11, x10
       add x10, x13, x10
       sw x9, 0(x10)
       jal x0, kernel_triangle_epilog
 kernel_triangle_block18:
       jal x0, kernel_triangle_epilog
 kernel_triangle_splitted_block_1:
       addi x14, x0, 2
       addi x13, x0, 4
       mul x13, x14, x13
       add x9, x9, x13
       lw x9, 0(x9)
       mulf x9, x12, x9
       addf x9, x11, x9
       sw x9, 0(x17)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 4060
       add x12, x8, x9
       addi x11, x0, 0
       addi x9, x0, 4
       mul x9, x11, x9
       add x9, x12, x9
       lw x16, 0(x9)
       lui, x11, 0
       lmi, x11, 0
       lli, x11, 2048
       add x11, x8, x11
       lw x9, 0(x11)
       addi x12, x9, 16
       addi x11, x0, 2
       addi x9, x0, 12
       mul x9, x11, x9
       add x12, x12, x9
       addi x11, x0, 0
       addi x9, x0, 4
       mul x9, x11, x9
       add x9, x12, x9
       lw x15, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 4060
       add x12, x8, x9
       addi x11, x0, 1
       addi x9, x0, 4
       mul x9, x11, x9
       add x9, x12, x9
       lw x14, 0(x9)
       lui, x11, 0
       lmi, x11, 0
       lli, x11, 2048
       add x11, x8, x11
       lw x9, 0(x11)
       addi x12, x9, 16
       addi x11, x0, 2
       addi x9, x0, 12
       mul x9, x11, x9
       add x12, x12, x9
       addi x11, x0, 1
       addi x9, x0, 4
       mul x9, x11, x9
       add x9, x12, x9
       lw x13, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 4060
       add x12, x8, x9
       addi x11, x0, 2
       addi x9, x0, 4
       mul x9, x11, x9
       add x9, x12, x9
       lw x12, 0(x9)
       lui, x11, 0
       lmi, x11, 0
       lli, x11, 2048
       add x11, x8, x11
       lw x9, 0(x11)
       addi x18, x9, 16
       addi x11, x0, 2
       addi x9, x0, 12
       mul x9, x11, x9
       add x18, x18, x9
       addi x11, x0, 2
       addi x9, x0, 4
       mul x9, x11, x9
       add x9, x18, x9
       lw x11, 0(x9)
       addi x9, x17, 4
       mulf x15, x16, x15
       mulf x13, x14, x13
       addf x13, x15, x13
       mulf x11, x12, x11
       addf x11, x13, x11
       sw x11, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 4048
       add x12, x8, x9
       addi x11, x0, 0
       addi x9, x0, 4
       mul x9, x11, x9
       add x9, x12, x9
       lw x9, 0(x9)
       lui, x12, 55
       lmi, x12, 636
       lli, x12, 1452
       global float32_neg
       jal x1, float32_neg
       bltf 1, x9, x10, 0
       bgef 2, x9, x10, 0
       jal x0, kernel_triangle_block3
 kernel_triangle_epilog:
       lw x9, 0(x8)
       lui, x11, 0
       lmi, x11, 0
       lli, x11, 128
       add x11, x8, x11
       lw x18, 0(x11)
       lui, x11, 0
       lmi, x11, 0
       lli, x11, 128
       add x11, x2, x11
       lw x1, 0(x11)
       lw x8, 0(x2)
       lui, x11, 0
       lmi, x11, 0
       lli, x11, 3088
       add x2, x2, x11
       jalr x0,x1, 0
       .align 4
