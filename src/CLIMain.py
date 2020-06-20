import sys
import os
import datetime 
import random
import click

from BoogieParser import *
from SVMLearn import *

#from SVMLearnMulti import *

@click.group(help="\"python3 CLIMain.py COMMAND --help\" for more details")
def cli():
    pass





@click.command()
@click.argument("source")
@click.argument("outfile", default = "temp.bpl")
def parseCtoBoogie(source, outfile):
    os.system("cpp " + source + " | grep -v '^#' | python3 ./C2Boogie.py stdin " + outfile + " --skip-methods __VERIFIER_error __VERIFIER_assert __VERIFIER_assume --assert-method __VERIFIER_assert --assume-method __VERIFIER_assume --add-trivial-invariants")

@click.command()
@click.argument("source")
@click.argument("outfile", default="OneLoop.py")
def parseCtoPy(source, outfile):
    os.system("cpp " + source + " | grep -v '^#' | python3 ./C2Boogie.py stdin temp.bpl --skip-methods __VERIFIER_error __VERIFIER_assert __VERIFIER_assume --assert-method __VERIFIER_assert --assume-method __VERIFIER_assume --add-trivial-invariants")
    parseBoogieProgramMulti("temp.bpl", outfile)

@click.command()
@click.argument("source")
@click.argument("parseoutfile", default="OneLoop.py")
def parseBoogie(source, parseoutfile):
    parseBoogieProgramMulti(source, parseoutfile)

@click.command()
@click.argument("source")
@click.option("--depth_bound", default=2, help="depth bound default set to 2")
@click.option("--filetype", type = click.Choice(["C", "BOOGIE"], False), default="BOOGIE", help="--file C: input is c file.\n --file BOOGIE: input is boogie file.\n default set to BOOGIE")
@click.option("--sample_strategy", type = click.Choice(["ENLARGE", "CONSTRAINT"], False), default="ENLARGE", help="--sample_strategy ENLARGE: enlarge the sample zone when sample num not enough.\n\
                                                                                                                   --sample_strategy CONSTRAINT: find feasible points by constraint if sample num not enough\n\
                                                                                                                   default set to ENLARGE")
@click.option("--cutting_strategy", type = click.Choice(["NEG", "MINI", "POS"], False), default="MINI", help="use f(x) < b to cut\n\
                                                                                                                --cutting_strategy POS:  b is a postive number\n\
                                                                                                                --cutting_strategy NEG: b is a negative number\n\
                                                                                                                --cutting_strategy MINI: b is the minimum value of sampled points\n\
                                                                                                                default set to MINI")
@click.option("--template_strategy", type = click.Choice(["SINGLEFULL", "FULL"], False), default="SINGLEFULL", help="templates used for learning\n\
                                                                                                                     --template_strategy SINGLEFULL: templates are either single variable or combination of all variables\n\
                                                                                                                     --template_strategy FULL: template is combination of all variables\n\
                                                                                                                     default set to SINGLEFULL")

@click.option("--print_level", type = click.Choice(["DEBUG", "INFO", "NONE"], False),  default="NONE", help="--print_level DEBUG: print all the information of the learning and debugging\n\
                                                                                           --print_level INFO: print the information of the learning\n\
                                                                                           --print_level NONE: only print the result information of the learning\n\
                                                                                           default set to NONE")
def lMulti(source, depth_bound, filetype, sample_strategy, cutting_strategy, template_strategy, print_level):
    print_level = 0 if print_level == "NONE" else 1 if print_level == "INFO" else 2 if print_level == "DEBUG" else "NONE"
    if filetype == "BOOGIE":
        sourceFilePath, sourceFileName,\
        templatePath, templateFileName, Info, \
        parse_oldtime, parse_newtime = parseBoogieProgramMulti(source, "OneLoop.py")
        from OneLoop import L
        result, rf_list = SVMLearnMulti(sourceFilePath, sourceFileName, 
                                        depth_bound,
                                        parse_oldtime, parse_newtime, 
                                        sample_strategy, cutting_strategy, template_strategy,
                                        print_level)
        if print_level == 0:
            printSummary(len(rf_list), result, rf_list, True)
    elif filetype == "C":
        os.system("python3 ./CPreprocess.py " + source)
        os.system("cpp " + source + " | grep -v '^#' | python3 ./C2Boogie.py stdin " + "temp.bpl" + " --skip-methods __VERIFIER_error __VERIFIER_assert __VERIFIER_assume --assert-method __VERIFIER_assert --assume-method __VERIFIER_assume --add-trivial-invariants")
        sourceFilePath, sourceFileName,\
        templatePath, templateFileName, Info, \
        parse_oldtime, parse_newtime = parseBoogieProgramMulti("temp.bpl", "OneLoop.py")
        result, rf_list = SVMLearnMulti(sourceFilePath, sourceFileName, 
                                        depth_bound,
                                        parse_oldtime, parse_newtime, 
                                        sample_strategy, cutting_strategy, template_strategy,
                                        print_level)
        if print_level == 0:
            printSummary(len(rf_list), result, rf_list, True)
        
    
@click.command()
@click.argument("source")
@click.option("--depth_bound", default=2, help="depth bound default set to 2")
@click.option("--filetype", type = click.Choice(["C", "BOOGIE"], False), default="BOOGIE", help="--file C: input is c file.\n --file BOOGIE: input is boogie file.\n default set to BOOGIE")
@click.option("--sample_strategy", type = click.Choice(["ENLARGE", "CONSTRAINT"], False), default="ENLARGE", help="--sample_strategy ENLARGE: enlarge the sample zone when sample num not enough.\n\
                                                                                                                   --sample_strategy CONSTRAINT: find feasible points by constraint if sample num not enough\n\
                                                                                                                   default set to ENLARGE")
@click.option("--print_level", type = click.Choice(["DEBUG", "INFO", "NONE"], False),  default="NONE", help="--print_level DEBUG: print all the information of the learning and debugging\n\
                                                                                           --print_level INFO: print the information of the learning\n\
                                                                                           --print_level NONE: only print the result information of the learning\n\
                                                                                           default set to NONE")
def lNested(source, depth_bound, filetype, sample_strategy, print_level):
    print_level = 0 if print_level == "NONE" else 1 if print_level == "INFO" else 2 if print_level == "DEBUG" else "NONE"
    if filetype == "BOOGIE":
        sourceFilePath, sourceFileName, templatePath, templateFileName, Info, parse_oldtime, parse_newtime = parseBoogieProgramNested(source, "OneLoop.py")
        from OneLoop import L
        result, rf_list = SVMLearnNested(sourceFilePath, sourceFileName, 
                                         depth_bound,
                                         templatePath, templateFileName, Info, 
                                         parse_oldtime, parse_newtime, sample_strategy, 
                                         print_level)
        if print_level >= 0:
            printSummaryNested(result, rf_list)
    elif filetype == "C":
        os.system("python3 CPreprocess.py " + source)
        os.system("cpp " + source + " | grep -v '^#' | python3 ./C2Boogie.py stdin " + "temp.bpl" + " --skip-methods __VERIFIER_error __VERIFIER_assert __VERIFIER_assume --assert-method __VERIFIER_assert --assume-method __VERIFIER_assume --add-trivial-invariants")
        sourceFilePath, sourceFileName,\
        templatePath, templateFileName, Info, \
        parse_oldtime, parse_newtime = parseBoogieProgramMulti("temp.bpl", "OneLoop.py")
        result, rf_list = SVMLearnNested(sourceFilePath, sourceFileName, 
                                         depth_bound,
                                         templatePath, templateFileName, Info, 
                                         parse_oldtime, parse_newtime, sample_strategy, 
                                         print_level)
        if print_level >= 0:
            printSummaryNested(result, rf_list)

cli.add_command(parseBoogie)
cli.add_command(lNested)
cli.add_command(lMulti)
cli.add_command(parseCtoBoogie)
cli.add_command(parseCtoPy)

if __name__ == '__main__':
    print("SVMRanker --- Version 1.0")
    cli()

