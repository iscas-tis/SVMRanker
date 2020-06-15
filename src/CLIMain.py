import sys
import os
import datetime 
import random
import click

from BoogieParser import *
from SVMLearn import *
from CPreprocessor import preprocessCFile

#from SVMLearnMulti import *

@click.group()
def cli():
    pass



@click.command(help="SOURCE: path of source c file OUTFILE: path of output boogie file, default set to temp.bpl")
@click.argument("source")
@click.argument("outfile", default = "temp.bpl")
def parseCtoBoogie(source, outfile):
    os.system("cpp " + source + " | grep -v '^#' | python3 ./C2Boogie.py stdin " + outfile + " --skip-methods __VERIFIER_error __VERIFIER_assert __VERIFIER_assume --assert-method __VERIFIER_assert --assume-method __VERIFIER_assume --add-trivial-invariants")

@click.command(help="SOURCE: path of source c file OUTFILE: path of output python file, default set to OneLoop.py")
@click.argument("source")
@click.argument("outfile", default="OneLoop.py")
def parseCtoPy(source, outfile):
    os.system("cpp " + source + " | grep -v '^#' | python3 ./C2Boogie.py stdin temp.bpl --skip-methods __VERIFIER_error __VERIFIER_assert __VERIFIER_assume --assert-method __VERIFIER_assert --assume-method __VERIFIER_assume --add-trivial-invariants")
    parseBoogieProgramMulti("temp.bpl", outfile)

@click.command(help="SOURCE: path of source boogie file PARSEOUTFILE: ath of output python file, default set to OneLoop.py")
@click.argument("source")
@click.argument("parseoutfile", default="OneLoop.py")
def parseBoogie(source, parseoutfile):
    parseBoogieProgramMulti(source, parseoutfile)

@click.command(help='SOURCE: path of source program file \n\
                     LOG: path of log folder, default set to ./Log_temp\n\
                     DEPTH_BOUND: depth bound of multiphase ranking function, default set to 2' )
@click.argument("source")
@click.argument('log', default=("./Log_temp"))
@click.argument("depth_bound", default=2)
@click.option("--filetype", type = click.Choice(["C", "BOOGIE"], False), default="BOOGIE", help="--file C: input is c file. --file BOOGIE: input is boogie file")
@click.option("--sample_strategy", type = click.Choice(["ENLARGE", "CONSTRAINT"], False), default="ENLARGE", help="--sample_strategy ENLARGE: enlarge the sample zone when sample num not enough.\n\
                                                                                                                   --sample_strategy CONSTRAINT: find feasible points by constraint if sample num not enough\n")
@click.option("--cutting_strategy", type = click.Choice(["MINUS", "MINI", "POS"], False), default="MINI", help="use f(x) < b to cut\n\
                                                                                                                --cutting_strategy POS:  b is a postive number\n\
                                                                                                                --cutting_strategy MINUS: b is a negative number\n\
                                                                                                                --cutting_strategy MINI: b is the minimum value of sampled points\n")
@click.option("--template_strategy", type = click.Choice(["SINGLEFULL", "FULL"], False), default="SINGLEFULL", help="templates used for learning\n\
                                                                                                                     --template_strategy SINGLEFULL: templates are either single variable or combination of all variables\n")

@click.option("--print_all", type = click.Choice(["T", "F"], False),  default="F", help="--print_all T: print all the information of the learning\n\
                                                                                         --print_all F: only print the result information of the learning\n")
def lMulti(source, log, depth_bound, filetype, sample_strategy, cutting_strategy, template_strategy, print_all):
    print("Learn Multiphase Ranking Function: " + sample_strategy + " " + cutting_strategy + " " + template_strategy)
    print_all = (True if print_all == "T" else False)
    if filetype == "BOOGIE":
        os.system("mkdir " + log)
        sourceFilePath, sourceFileName,\
        templatePath, templateFileName, Info, \
        parse_oldtime, parse_newtime = parseBoogieProgramMulti(source, "OneLoop.py")
        from OneLoop import L
        result, rf_list = SVMLearnMulti(sourceFilePath, sourceFileName, 
                                        log, depth_bound,
                                        parse_oldtime, parse_newtime, 
                                        sample_strategy, cutting_strategy, template_strategy,
                                        print_all)
        if not print_all:
            printSummary(len(rf_list), result, rf_list)
    elif filetype == "C":
        os.system("cpp " + source + " | grep -v '^#' | python3 ./C2Boogie.py stdin " + "temp.bpl" + " --skip-methods __VERIFIER_error __VERIFIER_assert __VERIFIER_assume --assert-method __VERIFIER_assert --assume-method __VERIFIER_assume --add-trivial-invariants")
        os.system("mkdir " + log)
        sourceFilePath, sourceFileName,\
        templatePath, templateFileName, Info, \
        parse_oldtime, parse_newtime = parseBoogieProgramMulti("temp.bpl", "OneLoop.py")
        result, rf_list = SVMLearnMulti(sourceFilePath, sourceFileName, 
                                        log, depth_bound,
                                        parse_oldtime, parse_newtime, 
                                        sample_strategy, cutting_strategy, template_strategy,
                                        print_all)
        if not print_all:
            printSummary(len(rf_list), result, rf_list)
        
    
@click.command(help='SOURCE: path of source program file LOG: path of log folder, default set to ./Log_temp')
@click.argument("source")
@click.argument('log', default=("./Log_temp"))
@click.option('--filetype', type = click.Choice(["C", "BOOGIE"], False), default="BOOGIE", help="--file C: input is c file. --file BOOGIE: input is boogie file")
@click.option("--sample_strategy", type = click.Choice(["ENLARGE", "CONSTRAINT"], False), default="ENLARGE", help="--sample_strategy ENLARGE: enlarge the sample zone when sample num not enough.\n\
                                                                                                                     --sample_strategy CONSTRAINT: find feasible points by constraint if sample num not enough\n")
@click.option("--print_all", type = click.Choice(["T", "F"], False),  default="F", help="--print_all T: print all the information of the learning\n\
                                                                                         --print_all F: only print the result information of the learning\n")

def lNested(source, log, filetype, sample_strategy, print_all):
    print_all = (True if print_all == "T" else False)
    if filetype == "BOOGIE":
        os.system("mkdir " + log)
        sourceFilePath, sourceFileName, templatePath, templateFileName, Info, parse_oldtime, parse_newtime = parseBoogieProgramNested(source, "OneLoop.py")
        from OneLoop import L
        result, rf_list = SVMLearnNested(sourceFilePath, sourceFileName, 
                                         templatePath, templateFileName, Info, log, 
                                         parse_oldtime, parse_newtime, sample_strategy, 
                                         print_all)
        if not print_all:
            printSummary(len(rf_list), result, rf_list)
    elif filetype == "C":
        os.system("cpp " + source + " | grep -v '^#' | python3 ./C2Boogie.py stdin " + "temp.bpl" + " --skip-methods __VERIFIER_error __VERIFIER_assert __VERIFIER_assume --assert-method __VERIFIER_assert --assume-method __VERIFIER_assume --add-trivial-invariants")
        os.system("mkdir " + log)
        sourceFilePath, sourceFileName,\
        templatePath, templateFileName, Info, \
        parse_oldtime, parse_newtime = parseBoogieProgramMulti("temp.bpl", "OneLoop.py")
        result, rf_list = SVMLearnNested(sourceFilePath, sourceFileName, 
                                         templatePath, templateFileName, Info, log, 
                                         parse_oldtime, parse_newtime, sample_strategy, 
                                         print_all)
        if not print_all:
            printSummary(len(rf_list), result, rf_list)

cli.add_command(parseBoogie)
cli.add_command(lNested)
cli.add_command(lMulti)
cli.add_command(parseCtoBoogie)
cli.add_command(parseCtoPy)

if __name__ == '__main__':
    print("SVMRanker --- Version 1.0")
    cli()

