import os
import sys
import re

StartDir = sys.argv[1]

fileList = os.listdir(StartDir)
for name in fileList:
    if name.endswith(".c"):
        print(name)
        with open(StartDir + name, "r", encoding="utf-8") as f:
            allLines = f.readlines()
            f.close()
        with open(StartDir + name, "w+", encoding="utf-8") as f:
            for eachline in allLines:
                eachline = eachline.replace("__VERIFIER_nondet_int()", "0")
                eachline = eachline.replace("extern int __VERIFIER_nondet_int(void);", "")
                f.write(eachline)