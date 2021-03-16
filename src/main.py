
import getopt, sys
import lzma
import struct

from utils import *
from instruction import *



if __name__ == "__main__":
    trace_path = "../traces/dpc3_traces/600.perlbench_s-210B.champsimtrace.xz"
    trace_path = parse_args(sys.argv, trace_path)
    print("Reading from trace: "+trace_path)

    ## setting number of dest and src of an instruction
    NUM_DEST = 4
    NUM_SRC = 2
    instr_fmt = "=QBB"+str(NUM_DEST)+"B"+str(NUM_SRC)+"B"+str(NUM_DEST)+"Q"+str(NUM_SRC)+"Q"
    instr_len = struct.calcsize(instr_fmt)
    instr_unpack = struct.Struct(instr_fmt).unpack_from

    ## read traces
    instr = []
    with lzma.open(trace_path, "rb") as tf:
        while True:
            data = tf.read(instr_len)
            if not data:
                break
            s = instr_unpack(data)
            instr.append(s)

            curr_instr = Instruction(instr, num_dest=NUM_DEST, num_src=NUM_SRC, zero_init=False)
            curr_instr.print_instr()
            break


