#include <string>
#include <stdio.h>
#include <stdlib.h>
#include "trace_preprocess.hpp"

using namespace std;    

// translate queue context into vector
void IWQ::to_vector() {
    auto last_ld = inner_queue.crbegin()->second;
    std::vector<uint64_t> *new_data = new std::vector<uint64_t>;
    std::vector<bool> *new_label = new std::vector<bool>;

    for (auto it=inner_queue.cbegin(); it != inner_queue.cend(); it++) {
        new_data->push_back(it->second.ip);
        new_label->push_back(last_ld.check_mem_depend(it->second));
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

    assert (data.size() == label.size());

    for (uint i=0; i < data.size(); i++) {
        dos << "Data["<<i<<"]: ";
        los << "Label["<<i<<"]: ";
        for (uint j=0; j<data[i]->size(); j++) {
            dos << data[i]->at(j) << " ";
            los << label[i]->at(j) << " ";
        }
        dos<<std::endl;
        los<<std::endl;
    }
}