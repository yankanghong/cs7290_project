#include <string>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include "trace_preprocess.hpp"

using namespace std;


#define INSTRUCTION_WINDOW 100

int main(int argc, char **argv) {
    
    string trace_path = "../traces/dpc3_traces/600.perlbench_s-210B.champsimtrace.xz";
    string out_dir = "./";
    // get options from command line
    char c;
    while ((c = getopt (argc, argv, "t:o:")) != -1)
    switch(c) {
        case 't':
            if(optarg) trace_path = string(optarg);
            break;
        case 'o':
            if(optarg) out_dir = string(optarg);
            if (out_dir.back() != '/') out_dir += '/';
            break;            
        default:
            std::cerr<< "Unknown option -"<<c<<"\n";
            abort();        
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
    dos.open(tr_dat, std::ofstream::out);
    los.open(tr_lab, std::ofstream::out);

    FILE *trace_file = popen( gz_command.c_str() , "r" );
    INSTRUCTION trace_instr;
    uint instr_size = sizeof(SINST);
    int lcnt(0), mcnt(0);

    IWQ iwq(INSTRUCTION_WINDOW);

    // read PIN trace
    while (fread(&(trace_instr.instr), 1, instr_size, trace_file)) {
        // trace_instr.print_instr();
        trace_instr.set_attr();
        iwq.push(trace_instr);
        if (trace_instr.is_ld())
            iwq.to_vector();
        
        mcnt++;
        if (mcnt == 10000000) {
            lcnt ++;
            std::cout << "Finish " << lcnt <<"0M instructions...\n";
            // print lwq content 
            // iwq.print_queue(); 
            // iwq.data_size(); 
            iwq.output_to_file(dos, los); 
            mcnt = 0;
            // break;
        }

    }
    printf("Done reading traces, generate output...\n");
    iwq.output_to_file(dos, los);
    pclose(trace_file);
    dos.close();
    los.close();
    
    return 0;
}

