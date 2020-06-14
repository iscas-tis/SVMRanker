import sys
import os
import datetime 
import random
import click

from BoogieParser import *
from SVMLearn import *

#from SVMLearnMulti import *

@click.group()
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
@click.argument('log', default=("./Log_temp"))
@click.option("--sample_strategy", type = click.Choice(["ENLARGE", "CONSTRAINT"], False), default="ENLARGE")
@click.option("--cutting_strategy", type = click.Choice(["MINUS", "MINI", "POS"], False), default="MINI")
@click.option("--template_strategy", type = click.Choice(["SINGLEFULL", "FULL"], False), default="SINGLEFULL")

def lMultiB(source, log, sample_strategy, cutting_strategy, template_strategy):
    print("Learn Multiphase Ranking Function: " + sample_strategy + " " + cutting_strategy + " " + template_strategy)
    os.system("mkdir " + log)
    sourceFilePath, sourceFileName, templatePath, templateFileName, Info, parse_oldtime, parse_newtime = parseBoogieProgramMulti(source, "OneLoop.py")
    from OneLoop import L
    result, rf_list = SVMLearnMulti(sourceFilePath, sourceFileName, 
                                    log, 
                                    parse_oldtime, parse_newtime, 
                                    sample_strategy, cutting_strategy, template_strategy)
    printSummary(len(rf_list), result, rf_list)
    
@click.command()
@click.argument("source")
@click.argument('log', default=("./Log_temp"))
@click.argument("sample_strategy", type = click.Choice(["ENLARGE", "CONSTRAINT"], False), default="ENLARGE")
def lNestedB(source, log, sample_strategy):
    os.system("mkdir " + log)
    sourceFilePath, sourceFileName, templatePath, templateFileName, Info, parse_oldtime, parse_newtime = parseBoogieProgramNested(source, "OneLoop.py")
    from OneLoop import L
    result, rf_list = SVMLearnNested(sourceFilePath, sourceFileName, templatePath, templateFileName, Info, log, parse_oldtime, parse_newtime, sample_strategy)
    printSummary(len(rf_list), result, rf_list)


cli.add_command(parseBoogie)
cli.add_command(lNestedB)
cli.add_command(lMultiB)

cli.add_command(parseCtoBoogie)
cli.add_command(parseCtoPy)

if __name__ == '__main__':
    print("SVMRanker -- Version 1.0")
    cli()

