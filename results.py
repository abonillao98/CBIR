import os
import numpy as np
import re

'''
Given a match file, this script shows the overall performances of the CBIR according with
the precision/recall measures and the F-score
'''

matches_file = "matches2.txt"

f = open(matches_file)
all_matches = f.read()
f.close()


lines = all_matches.count('\n')
querys = int(lines/12)

f = open(matches_file)
for x in range(0,querys):
    print("query number " + str(x))
    matches=[]
    for x in range(0,12):
        a = re.findall(r'\d+', f.readline())
        if a:
            matches.append(int(a[0]))
            
    print(matches)
    

        

    




