all: lab1_main

lab1_main: lab1.o lab1_main.o
	g++ -Wall -Werror -pedantic -o lab1_main lab1.o lab1_main.o

lab1.o: lab1.cpp lab1.h
	g++ -Wall -Werror -pedantic -c lab1.cpp

lab1_main.o: lab1_main.cpp lab1.h
	g++ -Wall -Werror -pedantic -c lab1_main.cpp

clean:
	rm -f *.o lab1_main
