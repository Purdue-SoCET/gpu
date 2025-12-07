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
       global kernel_pixel
       type kernel_pixel func
 kernel_pixel:
       lui, x11, 255
       lmi, x11, 4093
       lli, x11, 752
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
       lui, x11, 0
       lmi, x11, 0
       lli, x11, 256
       add x11, x8, x11
       sw x19, 0(x11)
       lui, x11, 0
       lmi, x11, 0
       lli, x11, 384
       add x11, x8, x11
       sw x20, 0(x11)
       lui, x11, 0
       lmi, x11, 0
       lli, x11, 512
       add x11, x8, x11
       sw x21, 0(x11)
       lui, x11, 0
       lmi, x11, 0
       lli, x11, 640
       add x11, x8, x11
       sw x22, 0(x11)
       lui, x11, 0
       lmi, x11, 0
       lli, x11, 768
       add x11, x8, x11
       sw x23, 0(x11)
       lui, x11, 0
       lmi, x11, 0
       lli, x11, 896
       add x11, x8, x11
       sw x24, 0(x11)
 kernel_pixel_block0:
       jal x0, kernel_pixel_block1
 kernel_pixel_block1:
       lui, x11, 0
       lmi, x11, 2
       lli, x11, 2432
       add x11, x8, x11
       sw x12, 0(x11)
       lui, x11, 0
       lmi, x11, 2
       lli, x11, 2432
       add x11, x8, x11
       lw x9, 0(x11)
       lui, x11, 0
       lmi, x11, 2
       lli, x11, 2304
       add x11, x8, x11
       sw x9, 0(x11)
       csrr x10, 1
       lui, x11, 0
       lmi, x11, 2
       lli, x11, 2304
       add x11, x8, x11
       lw x9, 0(x11)
       addi x9, x9, 16
       lw x12, 0(x9)
       csrr x9, 1
       lui, x11, 0
       lmi, x11, 2
       lli, x11, 2304
       add x11, x8, x11
       lw x11, 0(x11)
       addi x11, x11, 16
       lw x11, 0(x11)
       div x9, x9, x11
       mul x9, x12, x9
       sub x9, x10, x9
       lui, x11, 0
       lmi, x11, 2
       lli, x11, 2176
       add x11, x8, x11
       sw x9, 0(x11)
       csrr x10, 1
       lui, x11, 0
       lmi, x11, 2
       lli, x11, 2304
       add x11, x8, x11
       lw x9, 0(x11)
       addi x9, x9, 16
       lw x14, 0(x9)
       lui, x11, 0
       lmi, x11, 2
       lli, x11, 2304
       add x11, x8, x11
       lw x9, 0(x11)
       addi x9, x9, 20
       lw x13, 0(x9)
       csrr x9, 1
       lui, x11, 0
       lmi, x11, 2
       lli, x11, 2304
       add x11, x8, x11
       lw x11, 0(x11)
       addi x11, x11, 16
       lw x12, 0(x11)
       lui, x11, 0
       lmi, x11, 2
       lli, x11, 2304
       add x11, x8, x11
       lw x11, 0(x11)
       addi x11, x11, 20
       lw x11, 0(x11)
       div x10, x10, x14
       div x9, x9, x12
       div x9, x9, x11
       mul x9, x13, x9
       sub x9, x10, x9
       lui, x11, 0
       lmi, x11, 2
       lli, x11, 2048
       add x11, x8, x11
       sw x9, 0(x11)
       lui, x11, 0
       lmi, x11, 2
       lli, x11, 2304
       add x11, x8, x11
       lw x9, 0(x11)
       addi x9, x9, 28
       lw x10, 0(x9)
       csrr x9, 1
       addi x11, x0, 4
       mul x9, x9, x11
       add x9, x10, x9
       lw x9, 0(x9)
       lui, x11, 0
       lmi, x11, 2
       lli, x11, 1920
       add x11, x8, x11
       sw x9, 0(x11)
       lui, x11, 0
       lmi, x11, 2
       lli, x11, 1920
       add x11, x8, x11
       lw x9, 0(x11)
       addi x10, x0, 0
       blt 1, x9, x10, 0
       bge 2, x9, x10, 0
       jal x0, kernel_pixel_block3
 kernel_pixel_block2:
       lui, x11, 0
       lmi, x11, 2
       lli, x11, 2304
       add x11, x8, x11
       lw x9, 0(x11)
       addi x9, x9, 8
       lw x10, 0(x9)
       lui, x11, 0
       lmi, x11, 2
       lli, x11, 1920
       add x11, x8, x11
       lw x9, 0(x11)
       lui, x11, 255
       lmi, x11, 4095
       lli, x11, 3800
       add x12, x8, x11
       addi x11, x0, 12
       mul x9, x9, x11
       add x10, x10, x9
       lw x9, 0(x10)
       sw x9, 0(x12)
       lw x9, 4(x10)
       sw x9, 4(x12)
       lw x9, 8(x10)
       sw x9, 8(x12)
       addi x11, x8, -32
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3800
       add x10, x8, x9
       lw x9, 0(x10)
       sw x9, 0(x11)
       lw x9, 4(x10)
       sw x9, 4(x11)
       lw x9, 8(x10)
       sw x9, 8(x11)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 4048
       add x10, x8, x9
       lui, x9, 63
       lmi, x9, 0
       lli, x9, 0
       sw x9, 0(x10)
       lui, x11, 0
       lmi, x11, 2
       lli, x11, 2176
       add x11, x8, x11
       lw x9, 0(x11)
       itof x9, x9
       lui, x10, 255
       lmi, x10, 4095
       lli, x10, 4048
       add x10, x8, x10
       lw x10, 0(x10)
       lui, x11, 255
       lmi, x11, 4095
       lli, x11, 4052
       add x11, x8, x11
       addi x11, x11, 0
       addf x9, x9, x10
       sw x9, 0(x11)
       lui, x11, 0
       lmi, x11, 2
       lli, x11, 2048
       add x11, x8, x11
       lw x9, 0(x11)
       itof x9, x9
       lui, x10, 255
       lmi, x10, 4095
       lli, x10, 4048
       add x10, x8, x10
       lw x10, 0(x10)
       lui, x11, 255
       lmi, x11, 4095
       lli, x11, 4052
       add x11, x8, x11
       addi x11, x11, 4
       addf x9, x9, x10
       sw x9, 0(x11)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 4052
       add x9, x8, x9
       addi x10, x9, 8
       lui, x9, 63
       lmi, x9, 2048
       lli, x9, 0
       sw x9, 0(x10)
       lui, x11, 0
       lmi, x11, 2
       lli, x11, 2304
       add x11, x8, x11
       lw x9, 0(x11)
       addi x9, x9, 0
       lw x10, 0(x9)
       addi x9, x8, -32
       addi x9, x9, 0
       lw x9, 0(x9)
       lui, x11, 255
       lmi, x11, 4095
       lli, x11, 3988
       add x13, x8, x11
       addi x12, x0, 0
       addi x11, x0, 20
       mul x11, x12, x11
       add x12, x13, x11
       addi x11, x0, 20
       mul x9, x9, x11
       add x10, x10, x9
       lw x9, 0(x10)
       sw x9, 0(x12)
       lw x9, 4(x10)
       sw x9, 4(x12)
       lw x9, 8(x10)
       sw x9, 8(x12)
       lw x9, 12(x10)
       sw x9, 12(x12)
       lw x9, 16(x10)
       sw x9, 16(x12)
       lui, x11, 0
       lmi, x11, 2
       lli, x11, 2304
       add x11, x8, x11
       lw x9, 0(x11)
       addi x9, x9, 0
       lw x10, 0(x9)
       addi x9, x8, -32
       addi x9, x9, 4
       lw x9, 0(x9)
       lui, x11, 255
       lmi, x11, 4095
       lli, x11, 3988
       add x13, x8, x11
       addi x12, x0, 1
       addi x11, x0, 20
       mul x11, x12, x11
       add x12, x13, x11
       addi x11, x0, 20
       mul x9, x9, x11
       add x10, x10, x9
       lw x9, 0(x10)
       sw x9, 0(x12)
       lw x9, 4(x10)
       sw x9, 4(x12)
       lw x9, 8(x10)
       sw x9, 8(x12)
       lw x9, 12(x10)
       sw x9, 12(x12)
       lw x9, 16(x10)
       sw x9, 16(x12)
       lui, x11, 0
       lmi, x11, 2
       lli, x11, 2304
       add x11, x8, x11
       lw x9, 0(x11)
       addi x9, x9, 0
       lw x10, 0(x9)
       addi x9, x8, -32
       addi x9, x9, 8
       lw x9, 0(x9)
       lui, x11, 255
       lmi, x11, 4095
       lli, x11, 3988
       add x13, x8, x11
       addi x12, x0, 2
       addi x11, x0, 20
       mul x11, x12, x11
       add x12, x13, x11
       addi x11, x0, 20
       mul x9, x9, x11
       add x10, x10, x9
       lw x9, 0(x10)
       sw x9, 0(x12)
       lw x9, 4(x10)
       sw x9, 4(x12)
       lw x9, 8(x10)
       sw x9, 8(x12)
       lw x9, 12(x10)
       sw x9, 12(x12)
       lw x9, 16(x10)
       sw x9, 16(x12)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3952
       add x11, x8, x9
       addi x10, x0, 0
       addi x9, x0, 12
       mul x9, x10, x9
       add x12, x11, x9
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3988
       add x11, x8, x9
       addi x10, x0, 0
       addi x9, x0, 20
       mul x9, x10, x9
       add x9, x11, x9
       addi x10, x9, 0
       lw x9, 0(x10)
       sw x9, 0(x12)
       lw x9, 4(x10)
       sw x9, 4(x12)
       lw x9, 8(x10)
       sw x9, 8(x12)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3952
       add x11, x8, x9
       addi x10, x0, 1
       addi x9, x0, 12
       mul x9, x10, x9
       add x12, x11, x9
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3988
       add x11, x8, x9
       addi x10, x0, 1
       addi x9, x0, 20
       mul x9, x10, x9
       add x9, x11, x9
       addi x10, x9, 0
       lw x9, 0(x10)
       sw x9, 0(x12)
       lw x9, 4(x10)
       sw x9, 4(x12)
       lw x9, 8(x10)
       sw x9, 8(x12)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3952
       add x11, x8, x9
       addi x10, x0, 2
       addi x9, x0, 12
       mul x9, x10, x9
       add x12, x11, x9
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3988
       add x11, x8, x9
       addi x10, x0, 2
       addi x9, x0, 20
       mul x9, x10, x9
       add x9, x11, x9
       addi x10, x9, 0
       lw x9, 0(x10)
       sw x9, 0(x12)
       lw x9, 4(x10)
       sw x9, 4(x12)
       lw x9, 8(x10)
       sw x9, 8(x12)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3948
       add x10, x8, x9
       lui, x9, 63
       lmi, x9, 2048
       lli, x9, 0
       sw x9, 0(x10)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3944
       add x10, x8, x9
       lui, x9, 63
       lmi, x9, 2048
       lli, x9, 0
       sw x9, 0(x10)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3940
       add x10, x8, x9
       lui, x9, 63
       lmi, x9, 2048
       lli, x9, 0
       sw x9, 0(x10)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3952
       add x11, x8, x9
       addi x10, x0, 0
       addi x9, x0, 12
       mul x9, x10, x9
       add x9, x11, x9
       addi x9, x9, 0
       lw x9, 0(x9)
       lui, x10, 255
       lmi, x10, 4095
       lli, x10, 3936
       add x10, x8, x10
       sw x9, 0(x10)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3952
       add x11, x8, x9
       addi x10, x0, 1
       addi x9, x0, 12
       mul x9, x10, x9
       add x9, x11, x9
       addi x9, x9, 0
       lw x9, 0(x9)
       lui, x10, 255
       lmi, x10, 4095
       lli, x10, 3932
       add x10, x8, x10
       sw x9, 0(x10)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3952
       add x11, x8, x9
       addi x10, x0, 2
       addi x9, x0, 12
       mul x9, x10, x9
       add x9, x11, x9
       addi x9, x9, 0
       lw x9, 0(x9)
       lui, x10, 255
       lmi, x10, 4095
       lli, x10, 3928
       add x10, x8, x10
       sw x9, 0(x10)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3952
       add x11, x8, x9
       addi x10, x0, 0
       addi x9, x0, 12
       mul x9, x10, x9
       add x9, x11, x9
       addi x9, x9, 4
       lw x9, 0(x9)
       lui, x10, 255
       lmi, x10, 4095
       lli, x10, 3924
       add x10, x8, x10
       sw x9, 0(x10)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3952
       add x11, x8, x9
       addi x10, x0, 1
       addi x9, x0, 12
       mul x9, x10, x9
       add x9, x11, x9
       addi x9, x9, 4
       lw x9, 0(x9)
       lui, x10, 255
       lmi, x10, 4095
       lli, x10, 3920
       add x10, x8, x10
       sw x9, 0(x10)
       addi x9, x0, 4
       jal x0, kernel_pixel_splitted_block_1
 kernel_pixel_block3:
       jal x0, kernel_pixel_epilog
 kernel_pixel_block5:
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3848
       add x9, x8, x9
       lw x9, 0(x9)
       lui, x10, 0
       lmi, x10, 0
       lli, x10, 0
       bltf 1, x10, x9, 0
       bgef 2, x10, x9, 0
       jal x0, kernel_pixel_block9
 kernel_pixel_block6:
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3852
       add x9, x8, x9
       lw x9, 0(x9)
       lui, x10, 255
       lmi, x10, 4095
       lli, x10, 3844
       add x10, x8, x10
       sw x9, 0(x10)
       jal x0, kernel_pixel_block7
 kernel_pixel_block7:
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3852
       add x9, x8, x9
       lw x9, 0(x9)
       lui, x10, 255
       lmi, x10, 4095
       lli, x10, 3844
       add x11, x8, x10
       lui, x10, 0
       lmi, x10, 0
       lli, x10, 0
       subf x9, x10, x9
       sw x9, 0(x11)
       jal x0, kernel_pixel_block5
 kernel_pixel_block8:
       lui, x11, 0
       lmi, x11, 2
       lli, x11, 2304
       add x11, x8, x11
       lw x9, 0(x11)
       lui, x10, 0
       lmi, x10, 0
       lli, x10, 36
       add x9, x9, x10
       addi x9, x9, 0
       lw x9, 0(x9)
       addi x10, x0, 1
       sub x9, x9, x10
       itof x9, x9
       lui, x10, 255
       lmi, x10, 4095
       lli, x10, 3836
       add x10, x8, x10
       sw x9, 0(x10)
       lui, x11, 0
       lmi, x11, 2
       lli, x11, 2304
       add x11, x8, x11
       lw x9, 0(x11)
       lui, x10, 0
       lmi, x10, 0
       lli, x10, 36
       add x9, x9, x10
       addi x9, x9, 4
       lw x9, 0(x9)
       addi x10, x0, 1
       sub x9, x9, x10
       itof x9, x9
       lui, x10, 255
       lmi, x10, 4095
       lli, x10, 3832
       add x10, x8, x10
       sw x9, 0(x10)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3844
       add x9, x8, x9
       lw x10, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3844
       add x9, x8, x9
       lw x9, 0(x9)
       ftoi x9, x9
       itof x9, x9
       lui, x11, 255
       lmi, x11, 4095
       lli, x11, 3828
       add x11, x8, x11
       subf x9, x10, x9
       sw x9, 0(x11)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3840
       add x9, x8, x9
       lw x10, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3840
       add x9, x8, x9
       lw x9, 0(x9)
       ftoi x9, x9
       itof x9, x9
       lui, x11, 255
       lmi, x11, 4095
       lli, x11, 3824
       add x11, x8, x11
       subf x9, x10, x9
       sw x9, 0(x11)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3828
       add x9, x8, x9
       lw x10, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3836
       add x9, x8, x9
       lw x9, 0(x9)
       mulf x10, x10, x9
       lui, x9, 63
       lmi, x9, 0
       lli, x9, 0
       addf x9, x10, x9
       ftoi x9, x9
       lui, x10, 255
       lmi, x10, 4095
       lli, x10, 3820
       add x10, x8, x10
       sw x9, 0(x10)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3824
       add x9, x8, x9
       lw x10, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3832
       add x9, x8, x9
       lw x9, 0(x9)
       mulf x10, x10, x9
       lui, x9, 63
       lmi, x9, 0
       lli, x9, 0
       addf x9, x10, x9
       ftoi x9, x9
       lui, x10, 255
       lmi, x10, 4095
       lli, x10, 3816
       add x10, x8, x10
       sw x9, 0(x10)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3816
       add x9, x8, x9
       lw x11, 0(x9)
       lui, x11, 0
       lmi, x11, 2
       lli, x11, 2304
       add x11, x8, x11
       lw x9, 0(x11)
       lui, x10, 0
       lmi, x10, 0
       lli, x10, 36
       add x9, x9, x10
       addi x9, x9, 0
       lw x10, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3820
       add x9, x8, x9
       lw x9, 0(x9)
       lui, x12, 255
       lmi, x12, 4095
       lli, x12, 3812
       add x12, x8, x12
       mul x10, x11, x10
       add x9, x10, x9
       sw x9, 0(x12)
       lui, x11, 0
       lmi, x11, 2
       lli, x11, 2304
       add x11, x8, x11
       lw x9, 0(x11)
       lui, x10, 0
       lmi, x10, 0
       lli, x10, 32
       add x9, x9, x10
       lw x12, 0(x9)
       csrr x9, 1
       lui, x11, 0
       lmi, x11, 2
       lli, x11, 2304
       add x11, x8, x11
       lw x10, 0(x11)
       lui, x11, 0
       lmi, x11, 0
       lli, x11, 36
       add x10, x10, x11
       addi x10, x10, 8
       lw x11, 0(x10)
       lui, x10, 255
       lmi, x10, 4095
       lli, x10, 3812
       add x10, x8, x10
       lw x10, 0(x10)
       addi x13, x0, 12
       mul x9, x9, x13
       add x12, x12, x9
       addi x9, x0, 12
       mul x9, x10, x9
       add x10, x11, x9
       lw x9, 0(x10)
       sw x9, 0(x12)
       lw x9, 4(x10)
       sw x9, 4(x12)
       lw x9, 8(x10)
       sw x9, 8(x12)
       jal x0, kernel_pixel_epilog
 kernel_pixel_block9:
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3848
       add x9, x8, x9
       lw x9, 0(x9)
       lui, x10, 255
       lmi, x10, 4095
       lli, x10, 3840
       add x10, x8, x10
       sw x9, 0(x10)
       jal x0, kernel_pixel_block10
 kernel_pixel_block10:
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3848
       add x9, x8, x9
       lw x9, 0(x9)
       lui, x10, 255
       lmi, x10, 4095
       lli, x10, 3840
       add x11, x8, x10
       lui, x10, 0
       lmi, x10, 0
       lli, x10, 0
       subf x9, x10, x9
       sw x9, 0(x11)
       jal x0, kernel_pixel_block8
 kernel_pixel_splitted_block_1:
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3952
       add x11, x8, x9
       addi x10, x0, 2
       addi x9, x0, 12
       mul x9, x10, x9
       add x9, x11, x9
       addi x9, x9, 4
       lw x9, 0(x9)
       lui, x10, 255
       lmi, x10, 4095
       lli, x10, 3916
       add x10, x8, x10
       sw x9, 0(x10)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3948
       add x9, x8, x9
       lw x23, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3932
       add x9, x8, x9
       lw x22, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3916
       add x9, x8, x9
       lw x21, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3920
       add x9, x8, x9
       lw x20, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3928
       add x9, x8, x9
       lw x19, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3944
       add x9, x8, x9
       lw x18, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3936
       add x9, x8, x9
       lw x17, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3916
       add x9, x8, x9
       lw x16, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3928
       add x9, x8, x9
       lw x15, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3924
       add x9, x8, x9
       lw x14, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3940
       add x9, x8, x9
       lw x13, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3936
       add x9, x8, x9
       lw x12, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3920
       add x9, x8, x9
       lw x11, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3932
       add x9, x8, x9
       lw x10, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3924
       add x9, x8, x9
       lw x9, 0(x9)
       lui, x24, 255
       lmi, x24, 4095
       lli, x24, 3912
       add x24, x8, x24
       mulf x21, x22, x21
       mulf x19, x20, x19
       subf x19, x21, x19
       mulf x19, x23, x19
       mulf x16, x17, x16
       mulf x14, x15, x14
       subf x14, x16, x14
       mulf x14, x18, x14
       subf x14, x19, x14
       mulf x11, x12, x11
       mulf x9, x10, x9
       subf x9, x11, x9
       mulf x9, x13, x9
       addf x9, x14, x9
       sw x9, 0(x24)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3912
       add x9, x8, x9
       lw x9, 0(x9)
       lui, x10, 255
       lmi, x10, 4095
       lli, x10, 3908
       add x11, x8, x10
       lui, x10, 63
       lmi, x10, 2048
       lli, x10, 0
       divf x9, x10, x9
       sw x9, 0(x11)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3932
       add x9, x8, x9
       lw x13, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3916
       add x9, x8, x9
       lw x12, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3920
       add x9, x8, x9
       lw x11, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3928
       add x9, x8, x9
       lw x10, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3908
       add x9, x8, x9
       lw x9, 0(x9)
       lui, x14, 255
       lmi, x14, 4095
       lli, x14, 3904
       add x14, x8, x14
       mulf x12, x13, x12
       mulf x10, x11, x10
       subf x10, x12, x10
       mulf x9, x10, x9
       sw x9, 0(x14)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3940
       add x9, x8, x9
       lw x13, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3920
       add x9, x8, x9
       lw x12, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3944
       add x9, x8, x9
       lw x11, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3916
       add x9, x8, x9
       lw x10, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3908
       add x9, x8, x9
       lw x9, 0(x9)
       lui, x14, 255
       lmi, x14, 4095
       lli, x14, 3900
       add x14, x8, x14
       mulf x12, x13, x12
       mulf x10, x11, x10
       subf x10, x12, x10
       mulf x9, x10, x9
       sw x9, 0(x14)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3944
       add x9, x8, x9
       lw x13, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3928
       add x9, x8, x9
       lw x12, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3940
       add x9, x8, x9
       lw x11, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3932
       add x9, x8, x9
       lw x10, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3908
       add x9, x8, x9
       lw x9, 0(x9)
       lui, x14, 255
       lmi, x14, 4095
       lli, x14, 3896
       add x14, x8, x14
       mulf x12, x13, x12
       mulf x10, x11, x10
       subf x10, x12, x10
       mulf x9, x10, x9
       sw x9, 0(x14)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3928
       add x9, x8, x9
       lw x13, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3924
       add x9, x8, x9
       lw x12, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3936
       add x9, x8, x9
       lw x11, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3916
       add x9, x8, x9
       lw x10, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3908
       add x9, x8, x9
       lw x9, 0(x9)
       lui, x14, 255
       lmi, x14, 4095
       lli, x14, 3892
       add x14, x8, x14
       mulf x12, x13, x12
       mulf x10, x11, x10
       subf x10, x12, x10
       mulf x9, x10, x9
       sw x9, 0(x14)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3948
       add x9, x8, x9
       lw x13, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3916
       add x9, x8, x9
       lw x12, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3940
       add x9, x8, x9
       lw x11, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3924
       add x9, x8, x9
       lw x10, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3908
       add x9, x8, x9
       lw x9, 0(x9)
       lui, x14, 255
       lmi, x14, 4095
       lli, x14, 3888
       add x14, x8, x14
       mulf x12, x13, x12
       mulf x10, x11, x10
       subf x10, x12, x10
       mulf x9, x10, x9
       sw x9, 0(x14)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3940
       add x9, x8, x9
       lw x13, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3936
       add x9, x8, x9
       lw x12, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3948
       add x9, x8, x9
       lw x11, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3928
       add x9, x8, x9
       lw x10, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3908
       add x9, x8, x9
       lw x9, 0(x9)
       lui, x14, 255
       lmi, x14, 4095
       lli, x14, 3884
       add x14, x8, x14
       mulf x12, x13, x12
       mulf x10, x11, x10
       subf x10, x12, x10
       mulf x9, x10, x9
       sw x9, 0(x14)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3936
       add x9, x8, x9
       lw x13, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3920
       add x9, x8, x9
       lw x12, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3924
       add x9, x8, x9
       lw x11, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3932
       add x9, x8, x9
       lw x10, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3908
       add x9, x8, x9
       lw x9, 0(x9)
       lui, x14, 255
       lmi, x14, 4095
       lli, x14, 3880
       add x14, x8, x14
       mulf x12, x13, x12
       mulf x10, x11, x10
       subf x10, x12, x10
       mulf x9, x10, x9
       sw x9, 0(x14)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3924
       add x9, x8, x9
       lw x13, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3944
       add x9, x8, x9
       lw x12, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3948
       add x9, x8, x9
       lw x11, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3920
       add x9, x8, x9
       lw x10, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3908
       add x9, x8, x9
       lw x9, 0(x9)
       lui, x14, 255
       lmi, x14, 4095
       lli, x14, 3876
       add x14, x8, x14
       mulf x12, x13, x12
       mulf x10, x11, x10
       subf x10, x12, x10
       mulf x9, x10, x9
       sw x9, 0(x14)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3948
       add x9, x8, x9
       lw x13, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3932
       add x9, x8, x9
       lw x12, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3936
       add x9, x8, x9
       lw x11, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3944
       add x9, x8, x9
       lw x10, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3908
       add x9, x8, x9
       lw x9, 0(x9)
       lui, x14, 255
       lmi, x14, 4095
       lli, x14, 3872
       add x14, x8, x14
       mulf x12, x13, x12
       mulf x10, x11, x10
       subf x10, x12, x10
       mulf x9, x10, x9
       sw x9, 0(x14)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3904
       add x9, x8, x9
       lw x13, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3900
       add x9, x8, x9
       lw x12, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 4052
       add x9, x8, x9
       addi x9, x9, 0
       lw x11, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3896
       add x9, x8, x9
       lw x10, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 4052
       add x9, x8, x9
       addi x9, x9, 4
       lw x9, 0(x9)
       lui, x14, 255
       lmi, x14, 4095
       lli, x14, 3860
       add x14, x8, x14
       addi x14, x14, 0
       mulf x11, x12, x11
       addf x11, x13, x11
       mulf x9, x10, x9
       addf x9, x11, x9
       sw x9, 0(x14)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3892
       add x9, x8, x9
       lw x13, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3888
       add x9, x8, x9
       lw x12, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 4052
       add x9, x8, x9
       addi x9, x9, 0
       lw x11, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3884
       add x9, x8, x9
       lw x10, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 4052
       add x9, x8, x9
       addi x9, x9, 4
       lw x9, 0(x9)
       lui, x14, 255
       lmi, x14, 4095
       lli, x14, 3860
       add x14, x8, x14
       addi x14, x14, 4
       mulf x11, x12, x11
       addf x11, x13, x11
       mulf x9, x10, x9
       addf x9, x11, x9
       sw x9, 0(x14)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3880
       add x9, x8, x9
       lw x13, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3876
       add x9, x8, x9
       lw x10, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 4052
       add x9, x8, x9
       addi x9, x9, 0
       lw x9, 0(x9)
       lui, x11, 255
       lmi, x11, 4095
       lli, x11, 3860
       add x11, x8, x11
       addi x12, x11, 8
       mulf x11, x10, x9
       jal x0, kernel_pixel_splitted_block_4
 kernel_pixel_splitted_block_2:
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3872
       add x9, x8, x9
       lw x10, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 4052
       add x9, x8, x9
       addi x9, x9, 4
       lw x9, 0(x9)
       addf x11, x13, x11
       mulf x9, x10, x9
       addf x9, x11, x9
       sw x9, 0(x12)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3860
       add x9, x8, x9
       addi x9, x9, 0
       lw x14, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3988
       add x11, x8, x9
       addi x10, x0, 0
       addi x9, x0, 20
       mul x9, x10, x9
       add x9, x11, x9
       addi x9, x9, 0
       addi x9, x9, 8
       lw x13, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3860
       add x9, x8, x9
       addi x9, x9, 4
       lw x12, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3988
       add x11, x8, x9
       addi x10, x0, 1
       addi x9, x0, 20
       mul x9, x10, x9
       add x9, x11, x9
       addi x9, x9, 0
       addi x9, x9, 8
       lw x11, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3860
       add x9, x8, x9
       addi x9, x9, 8
       lw x10, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3988
       add x16, x8, x9
       addi x15, x0, 2
       addi x9, x0, 20
       mul x9, x15, x9
       add x9, x16, x9
       addi x9, x9, 0
       addi x9, x9, 8
       lw x9, 0(x9)
       lui, x15, 255
       lmi, x15, 4095
       lli, x15, 3856
       add x15, x8, x15
       mulf x13, x14, x13
       mulf x11, x12, x11
       addf x11, x13, x11
       mulf x9, x10, x9
       addf x9, x11, x9
       sw x9, 0(x15)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3860
       add x9, x8, x9
       addi x9, x9, 0
       lw x17, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3988
       add x11, x8, x9
       addi x10, x0, 0
       addi x9, x0, 20
       mul x9, x10, x9
       add x9, x11, x9
       addi x9, x9, 12
       lw x16, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3988
       add x11, x8, x9
       addi x10, x0, 0
       addi x9, x0, 20
       mul x9, x10, x9
       add x9, x11, x9
       addi x9, x9, 0
       addi x9, x9, 8
       lw x15, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3860
       add x9, x8, x9
       addi x9, x9, 4
       lw x14, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3988
       add x11, x8, x9
       addi x10, x0, 1
       addi x9, x0, 20
       mul x9, x10, x9
       add x9, x11, x9
       addi x9, x9, 12
       lw x13, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3988
       add x11, x8, x9
       addi x10, x0, 1
       addi x9, x0, 20
       mul x9, x10, x9
       add x9, x11, x9
       addi x9, x9, 0
       addi x9, x9, 8
       lw x12, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3860
       add x9, x8, x9
       addi x9, x9, 8
       lw x11, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3988
       add x18, x8, x9
       addi x10, x0, 2
       addi x9, x0, 20
       mul x9, x10, x9
       add x9, x18, x9
       addi x9, x9, 12
       lw x10, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3988
       add x19, x8, x9
       addi x18, x0, 2
       addi x9, x0, 20
       mul x9, x18, x9
       add x9, x19, x9
       addi x9, x9, 0
       addi x9, x9, 8
       lw x9, 0(x9)
       lui, x18, 255
       lmi, x18, 4095
       lli, x18, 3852
       add x18, x8, x18
       mulf x15, x16, x15
       mulf x15, x17, x15
       mulf x12, x13, x12
       mulf x12, x14, x12
       addf x12, x15, x12
       mulf x9, x10, x9
       mulf x9, x11, x9
       addf x9, x12, x9
       sw x9, 0(x18)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3852
       add x9, x8, x9
       lw x10, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3856
       add x9, x8, x9
       lw x9, 0(x9)
       lui, x11, 255
       lmi, x11, 4095
       lli, x11, 3852
       add x11, x8, x11
       divf x9, x10, x9
       sw x9, 0(x11)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3860
       add x9, x8, x9
       addi x9, x9, 0
       lw x16, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3988
       add x11, x8, x9
       addi x10, x0, 0
       addi x9, x0, 20
       mul x9, x10, x9
       add x9, x11, x9
       addi x9, x9, 16
       lw x15, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3988
       add x11, x8, x9
       addi x10, x0, 0
       addi x9, x0, 20
       mul x9, x10, x9
       add x9, x11, x9
       addi x9, x9, 0
       addi x9, x9, 8
       lw x14, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3860
       add x9, x8, x9
       addi x9, x9, 4
       lw x13, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3988
       add x11, x8, x9
       addi x10, x0, 1
       addi x9, x0, 20
       mul x9, x10, x9
       add x9, x11, x9
       addi x9, x9, 16
       lw x10, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3988
       add x12, x8, x9
       addi x11, x0, 1
       addi x9, x0, 20
       mul x9, x11, x9
       add x9, x12, x9
       addi x9, x9, 0
       addi x9, x9, 8
       lw x9, 0(x9)
       lui, x11, 255
       lmi, x11, 4095
       lli, x11, 3860
       add x11, x8, x11
       addi x11, x11, 8
       lw x12, 0(x11)
       lui, x11, 255
       lmi, x11, 4095
       lli, x11, 3988
       add x18, x8, x11
       addi x17, x0, 2
       addi x11, x0, 20
       mul x11, x17, x11
       add x11, x18, x11
       addi x11, x11, 16
       lw x11, 0(x11)
       mulf x14, x15, x14
       mulf x14, x16, x14
       mulf x9, x10, x9
       mulf x9, x13, x9
       addf x10, x14, x9
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3988
       add x14, x8, x9
       addi x13, x0, 2
       addi x9, x0, 20
       mul x9, x13, x9
       add x9, x14, x9
       addi x9, x9, 0
       addi x9, x9, 8
       jal x0, kernel_pixel_splitted_block_5
 kernel_pixel_splitted_block_3:
       lw x9, 0(x9)
       lui, x13, 255
       lmi, x13, 4095
       lli, x13, 3848
       add x13, x8, x13
       mulf x9, x11, x9
       mulf x9, x12, x9
       addf x9, x10, x9
       sw x9, 0(x13)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3848
       add x9, x8, x9
       lw x10, 0(x9)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3856
       add x9, x8, x9
       lw x9, 0(x9)
       lui, x11, 255
       lmi, x11, 4095
       lli, x11, 3848
       add x11, x8, x11
       divf x9, x10, x9
       sw x9, 0(x11)
       lui, x9, 255
       lmi, x9, 4095
       lli, x9, 3852
       add x9, x8, x9
       lw x9, 0(x9)
       lui, x10, 0
       lmi, x10, 0
       lli, x10, 0
       bltf 1, x10, x9, 0
       bgef 2, x10, x9, 0
       jal x0, kernel_pixel_block6
 kernel_pixel_splitted_block_4:
       jal x0, kernel_pixel_splitted_block_2
 kernel_pixel_splitted_block_5:
       jal x0, kernel_pixel_splitted_block_3
 kernel_pixel_epilog:
       lw x9, 0(x8)
       lui, x11, 0
       lmi, x11, 0
       lli, x11, 128
       add x11, x8, x11
       lw x18, 0(x11)
       lui, x11, 0
       lmi, x11, 0
       lli, x11, 256
       add x11, x8, x11
       lw x19, 0(x11)
       lui, x11, 0
       lmi, x11, 0
       lli, x11, 384
       add x11, x8, x11
       lw x20, 0(x11)
       lui, x11, 0
       lmi, x11, 0
       lli, x11, 512
       add x11, x8, x11
       lw x21, 0(x11)
       lui, x11, 0
       lmi, x11, 0
       lli, x11, 640
       add x11, x8, x11
       lw x22, 0(x11)
       lui, x11, 0
       lmi, x11, 0
       lli, x11, 768
       add x11, x8, x11
       lw x23, 0(x11)
       lui, x11, 0
       lmi, x11, 0
       lli, x11, 896
       add x11, x8, x11
       lw x24, 0(x11)
       lui, x11, 0
       lmi, x11, 0
       lli, x11, 128
       add x11, x2, x11
       lw x1, 0(x11)
       lw x8, 0(x2)
       lui, x11, 0
       lmi, x11, 2
       lli, x11, 3344
       add x2, x2, x11
       jalr x0,x1, 0
       .align 4
