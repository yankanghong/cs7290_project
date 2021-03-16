import numpy as np

class Instruction:
    """
        Instruction class

        Fields:
        - pc
        - is branch & branch taken:
        - dest_reg & src_reg
        - dest_mem & src_mem
    """
    def __init__(self, trace_instr, num_dest=4, num_src=2, zero_init=True):
        """
            Initializer for Instruction, default with zero_init
        """
        self.num_dest = num_dest
        self.num_src  = num_src
        if (zero_init):
            self.pc = 0
            self.is_br = 0
            self.br_tk = 0
            self.dest_reg = np.zeros(num_dest, dtype=np.uint8)
            self.src_reg = np.zeros(num_src, dtype=np.uint8)
            self.dest_mem = np.zeros(num_dest, dtype=np.uint64)
            self.src_mem = np.zeros(num_src, dtype=np.uint64)
        else:
            self.pc = trace_instr[0][0]
            self.is_br = trace_instr[0][1]
            self.br_tk = trace_instr[0][2]
            self.dest_reg = np.array(trace_instr[0][3:3+num_dest])
            self.src_reg = np.array(trace_instr[0][3+num_dest:3+num_dest+num_src])
            self.dest_mem = np.array(trace_instr[0][3+num_dest+num_src:3+2*num_dest+num_src])
            self.src_mem = np.array(trace_instr[0][3+2*num_dest+num_src:])

    def print_instr(self):
        print("PC:"+str(self.pc)+", is branch:"+str(self.is_br) +
              ", branch taken: " + str(self.br_tk))
        print("dest_reg:")
        print(self.dest_reg)
        print("src_reg:")
        print(self.src_reg)
        print("dest_mem:")
        print(self.dest_mem)
        print("src_mem:")
        print(self.src_mem)

