import csv
from matplotlib import pyplot as plt

with open('Single_E0vsEb.tsv') as tsvfile:
    reader = csv.reader(tsvfile, delimiter='\t')
    i=0
    E0=[]
    Eb=[]
    d0=[]
    for row in reader:
        if i>0:
            E0.append(float(row[0]))
            Eb.append(float(row[1]))
            d0.append(float(row[2]))
        i=i+1

plt.scatter(Eb, E0)

