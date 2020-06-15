import os
import sys
import re


def preprocessCFile(filepath):
    if filepath.endswith(".c"):
        with open(filepath, "r", encoding="utf-8") as f:
            allLines = f.readlines()
            f.close()
        with open(filepath, "w+", encoding="utf-8") as f:
            for eachline in allLines:
                eachline = eachline.replace("__VERIFIER_nondet_int()", "0")
                eachline = eachline.replace("extern int __VERIFIER_nondet_int(void);", "")
                f.write(eachline)
    else:
        print("ERROR: Not C File")