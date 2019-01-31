ravdebug:
	gcc -I/usr/local/include/gsl -O3 -c -g Stoch_SIR_Hetero.c
	gcc -L/usr/local/lib/ Stoch_SIR_Hetero.o -lgsl -lgslcblas -lm -o Stoch_SIR_Hetero


clean:
	rm -f *.o
	rm -f *.exe
	rm -f FixMCInt