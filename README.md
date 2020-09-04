# SVMRanker

## Introduction 

SVMRanker is a general framework for proving termination of loop programs.
SVMRanker utilizes SVM techniques to synthesize multiphase ranking functions to prove program termination. 


## Author

- Xuechao Sun
- Yong Li
- Xie Li

### Installation
You should have installed Python 3 and Java Development Kit on your system.
Currently we can successfully run SVMRanker with Python 3.7 and JDK 8.0.

**Install Python packages**

```
pip3 install z3-prover
pip3 install click
pip3 install sklearn
pip3 install python-constraint
```

### Usage
In the following, we assume that current directory is SVMRanker.

After having installed the required software, SVMRanker can be used by entering the **src/** directory and then calling SVMRanker as follows: 
```
  python3 ./CLIMain.py --help
```
You should be able to see the following output.
```
SVMRanker --- Version 1.0
Usage: CLIMain.py [OPTIONS] COMMAND [ARGS]...

  "python3 CLIMain.py COMMAND --help" for more details

Options:
  --help  Show this message and exit.

Commands:
  lmulti
  lnested
  parseboogie
  parsectoboogie
  parsectopy
```
As we can see, SVMRanker provides five commands. 
The first two commands allow for proving termination of a given program while the remaining three can be used for parsing the input file and translate it to a different format. 
In the remaining part of the section we focus on the details for the use of the **lmulti** and **lnested** commands.

**lmulti**, short for learning multiphase ranking function, instructs SVMRanker to learn a multiphase ranking function for the given program. 
To get the detailed usage information for this command, one can use the following command.
```
  python3 ./CLIMain.py lmulti --help
```
The output is the following.
```
SVMRanker --- Version 1.0
Usage: CLIMain.py lmulti [OPTIONS] SOURCE

Options:
  --depth_bound INTEGER           depth bound default set to 2
  --filetype [C|BOOGIE]           --file C: input is c file. --file BOOGIE:
                                  input is boogie file. default set to BOOGIE

  --sample_strategy [ENLARGE|CONSTRAINT]
                                  --sample_strategy ENLARGE: enlarge the
                                  sample zone when sample num not enough.
                                  --sample_strategy CONSTRAINT: find feasible
                                  points by constraint if sample num not
                                  enough default set to ENLARGE

  --cutting_strategy [NEG|MINI|POS]
                                  use f(x) < b to cut --cutting_strategy POS:
                                  b is a postive number --cutting_strategy
                                  NEG: b is a negative number
                                  --cutting_strategy MINI: b is the minimum
                                  value of sampled points default set to MINI

  --template_strategy [SINGLEFULL|FULL]
                                  templates used for learning
                                  --template_strategy SINGLEFULL: templates
                                  are either single variable or combination of
                                  all variables --template_strategy FULL:
                                  template is combination of all variables
                                  default set to SINGLEFULL

  --print_level [DEBUG|INFO|NONE]
                                  --print_level DEBUG: print all the
                                  information of the learning and debugging
                                  --print_level INFO: print the information of
                                  the learning --print_level NONE: only print
                                  the result information of the learning
                                  default set to NONE

  --help                          Show this message and exit.

```
As the help shows, there are several options available to tune the execution of **lmulti**; 
we present their usage by means of a couple of examples. 
```C
//example/Example1.c
	int main() {
    	int x, y;
    	while(x > 0 || y > 0) {
    		x = x + y - 1;
    		y = y - 1;
    	}
	}

```

The is the first C program we consider here; see the file **src/example/Example1.c**. 
This program can be shown to be terminating by means of a 2-multiphase ranking function, as we get by running SVMRanker to learn its multiphase ranking function as follows.
```
  python3 ./CLIMain.py lmulti --filetype C example/Example1.c
```
SVMRanker completes the analysis by returning a 2-multiphase ranking function for the **Example1.c** program, as shown below.
```
SVMRanker --- Version 1.0
example/Example1.c
--------------------LEARNING MULTIPHASE SUMMARY-------------------
MULTIPHASE DEPTH:  2
LEARNING RESULT:  TERMINATE
-----------RANKING FUNCTIONS----------
5.0 * 1 + 1.0 *  y^1 + 5.0 * 1
0.0796 *  x^1 + 0.482 * 1 + 0.482 * 1
```
Notice that we used the option **--filetype** to specify the type of the input program, given that SVMRanker supports both Boogie programs and C programs as input file, with the former being the default format. 
Furthermore, we can also provide the option **--depth_bound** to set the maximal number of phases SVMRanker can use when learning a multiphase ranking function. 
The default value of this option is 2, and this has been enough in the analysis of **Example1.c**, since **Example1.c** can be proved to terminate by a 2-multiphase ranking function. 
Such a default value is suitable for several programs, but it can be increased as needed, as we will see with the second example **src/example/Example2.c**, as shown below.
```C
	//example/Example2.c
	int main() {
    		int x, y, z;
    		while (x > 0) {
    			x = x + y;
    			y = y + z;
    			z = z - 1;
    		}	
	}
```
If we run SVMRanker on **Example2.c** with the default value of 2 for **--depth_bound**, we obtain **Unknown** as result. 
In order to get an appropriate multiphase ranking function for **Example2.c**, one needs to call **lmulti** with the option **--depth_bound** set to at least 3.
```
  python3 ./CLIMain.py lmulti --filetype C --depth_bound 3 example/Example2.c
```
With the help of **--depth_bound**, SVMRanker produces the result shown below.
```
SVMRanker --- Version 1.0
example/Example2.c
--------------------LEARNING MULTIPHASE SUMMARY-------------------
MULTIPHASE DEPTH:  3
LEARNING RESULT:  TERMINATE
-----------RANKING FUNCTIONS----------
2.0 * 1 + 2.0 * 1 + 1.0 *  z^1 + 2.0 * 1
1.0 * 1 + 0.2154 *  y^1 + 1.0 * 1 + 1.0 * 1
0.0911 *  x^1 + 0.3226 * 1 + 0.3226 * 1 + 0.3226 * 1
```
We now present the other options that let SVMRanker use different strategies in the process of learning a multiphase ranking function; 
different strategies regarding how program data points are sampled, how the state space is cut, and what templates are used, influence the running time of SVMRanker and possibly the final result. 

* **--sample_strategy**
	This option controls the strategy SVMRanker uses to sample program data points.
	Possible values are *CONSTRAINT* and *ENLARGE* (the default):
	*CONSTRAINT* samples randomly the points satisfying the loop condition/guard;
	This strategy can be slow as we need to get the assignments of variables satisfying the loop guard. 
	*ENLARGE* samples uniformly the points in a predefined space, which can be very efficient; However, if all the sampled points cannot satisfy the loop guard, we will then try to enlarge the sampling space until seeing some point satisfying the loop guard.

* **--cutting_strategy**
	This option controls the bound $b$ of the constraint f(x) < b that is used to cut the program state space in two parts for the current phase's decreasing function f.
	Possible values are *NEG*, *POS*, and *MINI* (the default):
	*NEG* chooses randomly a negative value for b;
	*POS* chooses randomly a positive value for b;
	*MINI* selects the minimum value of f on the sampled points.
* **--template_strategy** 
	This option controls what templates are used in the learning procedure.
	Possible values are *FULL* and *SINGLEFULL* (the default):
	*FULL* uses as templates the linear combinations of all program variables; 
	*SINGLEFULL* extends FULL with templates using only one variable at a time.

* **--print_level*
	This option controls the verbosity of the SVMRanker output.
	
	
The SVMRanker command **lnested**, short for learning nested ranking function, is used for learning a nested ranking function for a given program. 
The usage information of **lnested** can be obtained by the following command, with the output below.
 ```
 python3 ./CLIMain.py lnested --help
```
The output is the following.
```
SVMRanker --- Version 1.0
Usage: CLIMain.py lnested [OPTIONS] SOURCE

Options:
  --depth_bound INTEGER           depth bound default set to 2
  --filetype [C|BOOGIE]           --file C: input is c file. --file BOOGIE:
                                  input is boogie file. default set to BOOGIE

  --sample_strategy [ENLARGE|CONSTRAINT]
                                  --sample_strategy ENLARGE: enlarge the
                                  sample zone when sample num not enough.
                                  --sample_strategy CONSTRAINT: find feasible
                                  points by constraint if sample num not
                                  enough default set to ENLARGE

  --print_level [DEBUG|INFO|NONE]
                                  --print_level DEBUG: print all the
                                  information of the learning and debugging
                                  --print_level INFO: print the information of
                                  the learning --print_level NONE: only print
                                  the result information of the learning
                                  default set to NONE

  --help                          Show this message and exit.

```
As we can see, the options of **lnested** are also the ones of **lmulti**;
also the use of **lnested** is similar to the one of **lmulti**, just the outcome can be different.

For instance, we can prove termination of **Example2.c** by means of a learned nested ranking function by running SVMRanker as follows.
```
  python3 ./CLIMain.py lnested --filetype C --depth_bound 3 example/Example2.c
```
The output is shown below.
```
SVMRanker --- Version 1.0
example/Example2.c
--------------------LEARNING NESTED SUMMARY-------------------
NESTED DEPTH:  3
LEARNING RESULT:  TERMINATE
-----------RANKING FUNCTIONS----------
1.0 *  z^1.0 + 0.9 * 1; 1.0 *  y^1.0 + 0.9 * 1; 1.0 *  x^1.0 + 0.7 * 1

```
