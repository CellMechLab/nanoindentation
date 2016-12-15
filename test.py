# -*- coding: utf-8 -*-
"""
Created on Wed Dec 30 15:30:46 2015

@author: vassalli
"""
import matplotlib.pyplot as plt


def skiphead(f):
    riga = 'ciao ciao'
    while riga[0:4] != 'Time': 
        riga = f.readline()
        
def convertData(f):
    data = [[],[],[],[]]
    while True:
        riga = f.readline()
        if riga == '':
            break
        else:
            p = riga.replace('\n','').replace(',','.').split('\t')
            for i in range(2):
                data[i].append(float(p[i]))
            for i in range(2):
                data[i+2].append(float(p[i+3]))
    return data
    
def trovaPunti(time,vs):
    nodi = []
    nodi.append(0)
    j=0
    nexttime = vs[j][1]
    for i in range(len(time)):
        if i==len(time)-1:
            nodi.append(i)
        elif time[i]<=nexttime and time[i+1]>nexttime:
            nodi.append(i)
            if (j+1 == len(vs)):
                nodi.append(len(time)-1)
                break
            else:
                j+=1
                nexttime += vs[j][1]
    return nodi

def trovaPunti2(time,zeta,vs):
    nodi = []
    nodi.append(0)
    j=0
    nexttime = vs[j][1]
    nextvalue = vs[j][0]
    timefound = False
    valuefound = False
    for i in range(len(time)):
        if i==len(time)-1:
            nodi.append(i)
        else:
            if time[i]<=nexttime and time[i+1]>nexttime:
                timefound = True 
            if (zeta[i]<=nextvalue and zeta[i+1]>nextvalue) or (zeta[i]>=nextvalue and zeta[i+1]<nextvalue):
                valuefound = True
        if timefound and valuefound:
            nodi.append(i)
            nexttime = time[i]
            timefound=False
            valuefound=False
            if (j+1 == len(vs)):
                nodi.append(len(time)-1)
                break
            else:
                j+=1
                nexttime += vs[j][1]
                nextvalue = vs[j][0]
    return nodi

valori = [
    [0,0.5],[5000,2],[5000,1],[0,2],[0,0.5]
]

        
f = open('hFob_39gradi S-1 X-1 Y-1 I-1.txt')
skiphead(f)
all = convertData(f)
#nodi = trovaPunti(all[0],valori)
nodi = trovaPunti2(all[0],all[3],valori)

#plot(all[3],all[1])
#for k in nodi:    
#    plot(all[3][k],all[1][k],'ro')
for i in range(len(nodi)-1):
    plt.plot(all[3][nodi[i]:nodi[i+1]],all[1][nodi[i]:nodi[i+1]])
plt.show()
