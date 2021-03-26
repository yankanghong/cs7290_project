#include <string>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <thread>
#include <sys/types.h>
#include <thread>
#include <mutex>
#include <atomic>

#include "trace_preprocess.hpp"

using namespace std;


int main(int argc, char **argv) {
    
    string trace_path = "../../data/traces/dpc3_traces/600.perlbench_s-210B.champsimtrace.xz";
    string out_dir = "./";

    uint instr_window_size(DEFAULT_IW_SIZE);
    uint64_t max_num_instr(10000000);
    // get options from command line
    char c;
    while ((c = getopt (argc, argv, "t:o:w:n:")) != -1) {
        switch(c) {
            case 't': // path to input trace
                if(optarg) trace_path = string(optarg);
                break;
            case 'o': // output directory
                if(optarg) out_dir = string(optarg);
                if (out_dir.back() != '/') out_dir += '/';
                break; 
            case 'w': // instruction window size
                if (optarg) instr_window_size = atoll(optarg);    
                break;      
            case 'n': // maximum number of instructions
                if (optarg) max_num_instr = atoll(optarg);
                break;
            default:
                std::cerr<< "Unknown option -"<<c<<"\n";
                abort();        
        }
    }

    string trace_name(trace_path.substr(trace_path.find_last_of('/')+1));  
    std::cout << "Transforming trace: " << trace_name <<"\n";
    string tr_dat = out_dir+trace_name.substr(0, trace_name.find_last_of('.')) + ".dat";
    string tr_lab = out_dir+trace_name.substr(0, trace_name.find_last_of('.')) + ".lab";
    std::cout << "Output directory " << out_dir <<"\n";

    string gz_command = "xz -dc " + trace_path;
    
    srand(time(NULL));

    // output file
    std::ofstream dos, los;
    dos.open(tr_dat, std::ofstream::out | std::ios::binary);
    los.open(tr_lab, std::ofstream::out | std::ios::binary);

    FILE *trace_file = popen( gz_command.c_str() , "r" );
    INSTRUCTION trace_instr;
    uint instr_size = sizeof(SINST);
    int lcnt(0), mcnt(0);

    // The queue class 
    IWQ iwq(instr_window_size);

    // read PIN trace
    while (fread(&(trace_instr.instr), 1, instr_size, trace_file)) {
        // trace_instr.print_instr();
        trace_instr.set_attr();
        iwq.push(trace_instr);
        if (trace_instr.is_ld())
            iwq.to_vector();
        
        mcnt++;

        if ( ((mcnt%100000 == 0) || mcnt > max_num_instr) && mcnt) // output to file every 0.1M instructions
            iwq.output_to_file(dos, los); 
        
        if (mcnt == max_num_instr) {
            lcnt ++;
            std::cout << "Finish " << max_num_instr <<" instructions...\n";
            // print lwq content 
            // iwq.print_queue(); 
            // iwq.data_size(); 
            mcnt = 0;
            break;
        }
    }
    
    iwq.output_to_file(dos, los);
    printf("Done reading traces, output saves to \n\t%s \n\t%s \n", tr_dat.c_str(), tr_lab.c_str());
    pclose(trace_file);
    dos.close();
    los.close();
    
    return 0;
}

