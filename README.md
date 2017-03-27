# truss_optimizer

This small piece of code is prepared for creating simple truss population based on given set of parameters. 
Aim of the project is to create a genetic evolutionary algorithm to find the optimized truss geometry based on those constraints. 
Further tasks include:
Adding a simple structural analysis module
Adding a simple structural steel design module (AISC  360-10)
Creating TRUSS sample DNA's.
Adding a fitness function. This fitness function will be function of the weight of each member
At each generation, trusses will be sorted according to their fitness values. Algorithm will kill the bottom half of the population.
Then, by using the surviving truss DNA's, it will generate a new population.
Algorithm will reiterate until the population converges to an optimum solution.
