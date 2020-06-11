import sys
import os
import datetime 
import random
import click

from BoogieParser import *

#from SVMLearnMulti import *

@click.group()
def cli():
    pass


@click.command()
@click.argument("source")
@click.argument("outfile")
def parseBoogie(source, outfile):
    parseBoogieProgram(source, outfile)

@click.command()
@click.option("--learn", type=click.Choice(["nested", "multiphase"]), help="choice to learn multiphase- or nested- ranking function")
@click.argument("source")
@click.argument('log', default="temp.log")

def learnRanking(learn, source, log):
    print()

cli.add_command(learnRanking)
cli.add_command(parseBoogie)


if __name__ == '__main__':
    cli()

