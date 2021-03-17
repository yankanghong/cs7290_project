
import getopt, sys
import gzip, lzma, bz2
import struct
import queue

import models
from utils import *
from instruction import *

if __name__ == "__main__":
    trace_path = "../traces/dpc3_traces/600.perlbench_s-210B.champsimtrace.xz"
    model_name, trace_path = parse_args(sys.argv, trace_path)
    print("Reading from trace: "+trace_path)
    if (model_name == 'SimpleModel'):
        model  = SimpleModel()

    tf_ext = trace_path.split('.')[-1] # get file name extension
    if (tf_ext == 'gz'):
        myopen = gzip.open
    elif (tf_ext == 'xz'):
        myopen = lzma.open
    elif (tf_ext == 'bz2'):
        myopen = bz2.open
    else:
        myopen = open

    ## setting number of dest and src of an instruction
    NUM_DEST = 4
    NUM_SRC = 2
    instr_fmt = "=QBB"+str(NUM_DEST)+"B"+str(NUM_SRC)+"B"+str(NUM_DEST)+"Q"+str(NUM_SRC)+"Q"
    instr_len = struct.calcsize(instr_fmt)
    instr_unpack = struct.Struct(instr_fmt).unpack_from
    LQ_SIZE = 30
    SQ_SIZE = 30
    ldq = queue.Queue(maxsize=LQ_SIZE)
    stq = queue.Queue(maxsize=SQ_SIZE)
    
    ## read traces
    tf = myopen(trace_path, 'rb')
    minst_cnt = 0

    with tf:
        data = tf.read(instr_len)
        
        # instruction counter for calculating average wrong predictions over 1000 instructions
        instr_cnt = 0
        while (data != b""):
            instr = []
            s = instr_unpack(data)
            instr.append(s)
            instr_cnt += 1
            if (instr_cnt%1000000 == 0):
                minst_cnt += 1
                print(("Instruction Counter: {0}M instructions done...")
                    .format(minst_cnt))

            dest_mem = np.array(instr[0][3+NUM_DEST+NUM_SRC:3+2*NUM_DEST+NUM_SRC], dtype=np.uint64)
            src_mem = np.array(instr[0][3+2*NUM_DEST+NUM_SRC:], dtype=np.uint64)

            if (not np.any(dest_mem) and not np.any(src_mem)):
                # skip those not memory instructions
                data = tf.read(instr_len)
                continue

            # do some translation
            instr = list(instr[0])[0:3+NUM_DEST+NUM_SRC]
            instr.append(dest_mem)
            instr.append(src_mem)

            curr_instr = Instruction(instr, num_dest=NUM_DEST, num_src=NUM_SRC, zero_init=False)
            # curr_instr.print_instr()

            # put to LSQ
            if (curr_instr.is_st):
                if (stq.full()):
                    stq_head = stq.get()
                stq.put(curr_instr, block=False)

            if (curr_instr.is_ld):
                if (ldq.full()):
                    ldq_head = ldq.get()
                ldq.put(curr_instr, block=False)
                # train the model when instruction comes in 
                # acc = model.train(ldq, stq)

            data = tf.read(instr_len)




