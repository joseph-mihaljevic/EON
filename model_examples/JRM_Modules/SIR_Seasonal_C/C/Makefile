ravdebug:
	gcc -I/usr/local/include/gsl -O3 -c -g Seasonal_SIR.c
	gcc -L/usr/local/lib/ Seasonal_SIR.o -lgsl -lgslcblas -lm -o Seasonal_SIR


clean:
	rm -f *.o
	rm -f *.exe
	rm -f FixMCInt
