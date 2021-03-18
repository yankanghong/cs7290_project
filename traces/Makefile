DEBUG=-g -Wall
CFLAGS=-std=c++11 -O
CC=g++

# objects 
OBJECTS=main.o trace_preprocess.o 

all: trpr outputs_dir 
	mv *.o outputs
	@echo compile done...

trpr: $(OBJECTS)
	@$(CC) -o $@ $(CFLAGS) $(DEBUG) $(OBJECTS)

$(OBJECTS): %.o : %.cpp
	@$(CC) -c $(CFLAGS) $(DEBUG) $< -o $@

outputs_dir:
	mkdir -p outputs

.PHONY: clean
clean:
	rm -rf trpr *.o *.dat *.lab outputs/