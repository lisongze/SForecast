import sys, os
import numpy as np
import pandas as pd
import datetime

if __name__ == '__main__':
    infile = sys.argv[1]
    csv_content = pd.read_csv(infile, [0])
    date = []
