#include <string>
#include <stdio.h>
#include <stdlib.h>
#include "trace_preprocess.hpp"

using namespace std;    

// translate queue context into data vector
void IWQ::to_vector() {

    bool mem_depend(false);

    auto last_ld = inner_queue.crbegin()->second;
    std::shared_ptr<std::vector<uint64_t>> new_data (new std::vector<uint64_t>);
    std::shared_ptr<std::vector<bool>> new_label (new std::vector<bool>);

    for (auto it=inner_queue.cbegin(); it != inner_queue.cend(); it++) {
        mem_depend = last_ld.check_mem_depend(it->second);
        
        /* Having a random filtering mechanism to filter out 
        some no dependency vector to reduce the data size
           Only filter out those no-dependency
        */
        // if (!mem_depend && ((rand() % (100)) < int(FILTER_PROB*100))) 
            // continue;
        new_data->push_back(it->second.instr.ip);
        new_label->push_back(mem_depend);
    }

    uint vec_size = new_data->size();
    for (uint i=0; i<queue_size-vec_size; i++) {
        new_data->push_back(0); // pad 0
        new_label->push_back(0);
    }
    data.push_back(new_data);
    label.push_back(new_label);
}


void IWQ::output_to_file(ofstream &dos, ofstream&los) {
    // print out data size
    if (data.empty())
        return;
    assert (data.size() == label.size());
    std::cout<< "Number of data: " << data.size() << "\n";
    for (uint64_t i=0; i < data.size(); i++) {
        dos << "Data["<<i<<"]: ";
        los << "Label["<<i<<"]: ";
        for (uint64_t j=0; j<data[i]->size(); j++) {
            dos << data[i]->at(j) << " ";
            los << label[i]->at(j) << " ";
        }
        dos<<std::endl;
        los<<std::endl;
    }
    // remove data once saved to output
    data.clear();
    label.clear();

}