DEBUG=-g -Wall
CFLAGS=-std=c++11 -O3
CC=g++

# objects 
OBJECTS=main.to trace_preprocess.to 

all: trpr.o outputs_dir 
	@mv *.to outputs
	@echo Compile done...

trpr.o: $(OBJECTS)
	@$(CC) -o $@ $(CFLAGS) $(DEBUG) $(OBJECTS)

$(OBJECTS): %.to : %.cpp
	@$(CC) -c $(CFLAGS) $(DEBUG) $< -o $@

outputs_dir:
	@mkdir -p outputs

.PHONY: clean
clean:
	@rm -rf  *.o *.dat *.lab outputs/
