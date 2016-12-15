from scipy.signal import savgol_filter as savitzky_golay

def getSG(y,filtwidth=21,filtorder=2,deriv=1):
    filtwidth = int(filtwidth)
    if filtwidth < filtorder + 2:
        filtwidth = filtorder + 3
    if filtwidth % 2 == 0:
        filtwidth +=1
        #print 'WARN: window size reset to {0}'.format(filtwidth)
    try:
        o = savitzky_golay(y, filtwidth, filtorder, deriv=deriv)
    except:
        print( len(y),filtwidth,filtorder)
        return None
    return o

