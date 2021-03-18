#pragma once
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <string.h>
#include <inttypes.h>
#include <iostream>
#include <fstream>
#include <list>
#include <algorithm>
#include <utility>
#include <vector>


// #define NDEBUG

#include <assert.h>

// instruction format
#define ROB_SIZE 352
#define LQ_SIZE 128
#define SQ_SIZE 72
#define NUM_INSTR_DESTINATIONS_SPARC 4
#define NUM_INSTR_DESTINATIONS 2
#define NUM_INSTR_SOURCES 4

// special registers that help us identify branches
#define REG_STACK_POINTER 6
#define REG_FLAGS 25
#define REG_INSTRUCTION_POINTER 26

// branch types
#define NOT_BRANCH           0
#define BRANCH_DIRECT_JUMP   1
#define BRANCH_INDIRECT      2
#define BRANCH_CONDITIONAL   3
#define BRANCH_DIRECT_CALL   4
#define BRANCH_INDIRECT_CALL 5
#define BRANCH_RETURN        6
#define BRANCH_OTHER         7

class INSTRUCTION {
public:

    // instruction pointer or PC (Program Counter)
    uint64_t ip;

    // branch info
    uint8_t is_branch;
    uint8_t branch_taken;

    uint8_t destination_registers[NUM_INSTR_DESTINATIONS]; // output registers
    uint8_t source_registers[NUM_INSTR_SOURCES]; // input registers

    uint64_t destination_memory[NUM_INSTR_DESTINATIONS]; // output memory
    uint64_t source_memory[NUM_INSTR_SOURCES]; // input memory

    // constructor
    INSTRUCTION():ip(0), is_branch(0), branch_taken(0) {

        for (uint32_t i=0; i<NUM_INSTR_SOURCES; i++) {
            source_registers[i] = 0;
            source_memory[i] = 0;
        }

        for (uint32_t i=0; i<NUM_INSTR_DESTINATIONS_SPARC; i++) {
            destination_registers[i] = 0;
            destination_memory[i] = 0;
        }
    };

    void print_instr(){
        // instruction pointer or PC (Program Counter)
        printf("PC: %llu\n", ip);

        // branch info
        std::cout<< "is_branch: "<< static_cast<uint>(is_branch)<<std::endl;
        std::cout<< "branch_taken: "<< static_cast<uint>(branch_taken)<<std::endl;

        std::cout<< "dest regs:";
        for (uint i=0; i<NUM_INSTR_DESTINATIONS; i++)
            std::cout<< " " << uint(destination_registers[i]); // output registers
        std::cout<<std::endl;

        std::cout<< "src regs:";
        for (uint i=0; i<NUM_INSTR_SOURCES; i++)
            std::cout<< " " << uint(source_registers[i]); // input registers
        std::cout<<std::endl;        

        std::cout<< "dest mem:";
        for (uint i=0; i<NUM_INSTR_DESTINATIONS; i++)
            std::cout<< " " << destination_memory[i]; // output memory
        std::cout<<std::endl;   

        std::cout<< "src mem:";
        for (uint i=0; i<NUM_INSTR_SOURCES; i++)
            std::cout<< " " << source_memory[i]; // input memory
        std::cout<<std::endl;   

        // std::cout << "asid0: "<< static_cast<uint>(asid[0])<<std::endl;
        // std::cout<< "asid1: "<< static_cast<uint>(asid[1])<<std::endl;
    }

    // check if an instruction is load
    bool is_ld(){
        for (uint i=0; i<NUM_INSTR_SOURCES; i++)
            if (source_memory[i] != 0)
                return true;
        
        return false;
    }     

    // check if an instruction is store
    bool is_st(){
        for (uint i=0; i<NUM_INSTR_DESTINATIONS; i++)
            if (destination_memory[i] != 0)
                return true;
        
        return false;
    }   
    // check is an instruction is mem instr
    bool is_mem(){
        for (uint i=0; i<NUM_INSTR_SOURCES; i++)
            if (source_memory[i] != 0)
                return true;  
        for (uint i=0; i<NUM_INSTR_DESTINATIONS; i++)
            if (destination_memory[i] != 0)
                return true;
        
        return false;                      
    }

    // check if memory dependency exist, input would be a store instruction
    bool check_mem_depend(INSTRUCTION store) {
        if (!is_st())
            return false;

        for (uint i=0; i<NUM_INSTR_SOURCES; i++) {
            if (source_memory[i] == 0)
                continue;
            for (uint j=0; j<NUM_INSTR_DESTINATIONS; j++)
                if (source_memory[i] == store.destination_memory[j])
                    return true;
        }

        return false;
    }
};

class IWQ {
public:
    const uint queue_size;
    
    /* inner queue, each elem is an instruction and counter
        Only mem instruction is inserted
    */
    std::list<std::pair<uint, INSTRUCTION>> inner_queue;

    // vector to store data and label
    std::vector<std::vector<uint64_t> *> data;
    std::vector<std::vector<bool> *> label;

    // constructor, initial an empty queue with size
    IWQ(uint qsize):queue_size(qsize){}

    // deconstructor
    ~IWQ() {
        for (auto p:data)
            delete p;
        for (auto p:label)
            delete p;
    }

    // if a queue is full, it will automatically remove the head elem
    void push(INSTRUCTION instr){

        // if not empty, need to check overflow and add counter
        if (inner_queue.size()) {
            if (inner_queue.front().first == (queue_size-1))
                inner_queue.pop_front(); // remove the head instruction (too old)

            // add one for all instr in the queue
            for (auto it = inner_queue.begin(); it != inner_queue.end(); it++)
                it->first ++;
        }

        if (instr.is_mem())
            inner_queue.push_back(std::make_pair(0, instr));
        return;
    }

    bool is_full(){
        return (inner_queue.size() == queue_size);
    }

    void print_queue() {
        printf("Queue valid elem: %lu\n", inner_queue.size());
        for (auto it = inner_queue.begin(); it != inner_queue.end(); it++) {
            std::cout<< "The " <<it->first << "th instruction, detail: ";
            it->second.print_instr();
        }
    }

    // print out data size
    void data_size() {
        // print out data size
        std::cout<< data.size()<<std::endl;
        assert (data.size() == label.size());
    }

    // print out the data and label to ostream
    void output_to_file(std::ofstream &dos, std::ofstream &los);

    // translate the data into vector
    void to_vector();
};
