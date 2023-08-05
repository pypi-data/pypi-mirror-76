import os
def importer(name):
    data=open(name,"w")
    data.seek(0)
    data.write("""import os
import torch
import numpy
import math
import turtle
import openpyxl""")
    os.startfile(f"{name}.py")
    data.close()