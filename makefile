%.cpp.out: %.cpp
	g++ -g -o $@ $<
clean:
	rm -rf *.out
%.py.out: %.py
	cp $< $@
	chmod +x $@
