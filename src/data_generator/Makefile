
CXX=g++
DEBUG=-g -Wall
CPPFLAGS=-std=c++11 -O3 -pthread

# objects 
OBJECTS=main.to trace_preprocess.to 

all: trpr.o outputs_dir 
	@mv *.to outputs
	@echo Compile done...

trpr.o: $(OBJECTS)
	@$(CXX) -o $@ $(CPPFLAGS) $(DEBUG) $(OBJECTS) 

$(OBJECTS): %.to : %.cpp
	@$(CXX) -c $(CPPFLAGS) $(DEBUG) $< -o $@

outputs_dir:
	@mkdir -p outputs

.PHONY: clean
clean:
	@rm -rf  *.o *.dat *.lab outputs/
