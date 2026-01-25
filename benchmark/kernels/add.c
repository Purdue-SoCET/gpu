#include "include/kernel.h"
#include "include/add.h"

void kernel_add(void* arg) {
    add_arg_t* args = (add_arg_t*) arg;
    int i = blockIdx * blockDim + threadIdx;

    args->out[i] = args->a[i] + args->b[i];
}