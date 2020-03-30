import numpy as np
import random
from scipy.signal import find_peaks
from scipy.interpolate import interp1d
from scipy.optimize import curve_fit
from scipy.signal import savgol_filter
from matplotlib import pyplot as plt

class bsegment(object):
    def __init__(self,s=None,x=None,y=None):
        self.phase = 1
        self.z = None
        self.f = None
        self.R = None
        self.k = None
        if s is not None:
            if x is not None:
                self.z = x
            else:
                self.z = s.z
            if y is not None:
                self.f = y
            else:
                self.f = s.f
            self.R = s.parent.tip_radius
            self.k = s.parent.cantilever_k
        self.offsetY = 0
        self.offsetX = 0
        self.ffil = self.f
        self.indentation = None
        self.touch = None
        self.valid = True
        self.plit = None
        self.sigma = None
        self.epsilon = None
        self.EcurveInd = None #to store d of E(d) in raw mode 
        self.Ecurve = None    #to store E(d) obtained raw mode
        self.pressure = None  #to store P(d) for Manliography
        self.Elastx = None    #to store d of E(d) elastography mode
        self.Elasty = None    #to store E(d) obtained in elastography mode
        self.IndexDv = None   #aux indices
        self.E = None

def getMedCurve(xar,yar,loose = True,threshold=5):
    if loose is False:
        xmin = -np.inf
        xmax = np.inf
        deltax = 0
        for x in xar:
            xmin = np.max([xmin,np.min(x)])
            xmax = np.min([xmax,np.max(x)])
            deltax += ((np.max(x)-np.min(x))/len(x))
        deltax /= len(xar)
        xnew = np.linspace(xmin,xmax,int( (xmax-xmin)/deltax) )
        ynew = np.zeros(len(xnew))
        for i in range(len(xar)):
            ycur = np.interp(xnew, xar[i], yar[i])
            ynew += ycur
        ynew/=len(xar)
    else:
        xmin = np.inf
        xmax = -np.inf
        deltax = 0
        for x in xar:
            xmin = np.min([xmin,np.min(x)])
            xmax = np.max([xmax,np.max(x)])
            deltax += ((np.max(x)-np.min(x))/(len(x)-1))
        deltax /= len(xar)
        xnewall = np.linspace(xmin,xmax,int( (xmax-xmin)/deltax) )
        ynewall = np.zeros(len(xnewall))
        count = np.zeros(len(xnewall))
        for i in range(len(xar)):
            imin = np.argmin( (xnewall-np.min(xar[i]))**2 )#+1
            imax = np.argmin( (xnewall-np.max(xar[i]))**2 )#-1
            ycur = np.interp(xnewall[imin:imax], xar[i], yar[i])
            ynewall[imin:imax] += ycur
            count[imin:imax] += 1
        cc = count > threshold
        xnew = xnewall[cc]
        ynew = ynewall[cc]/count[cc]
    return xnew,ynew

def calculateSS(s,indentation=None,touch=None):
    # a = sqrt(R delta)
    # epsilon = 0.2 a/R = 0.2 sqrt(delta/R)
    # sigma = F / pi a^2 = F / (pi R delta) 
    if indentation is None:
        indentation = s.indentation
        touch = s.touch
    epsilon = 0.2*np.sqrt(indentation/s.R)
    sigma   = touch / np.pi/s.R/indentation 
    return epsilon,sigma 

def ElastoStrainSmart(epsilon,sigma,window = 101):
    if window%2 == 0:
        window+=1
    poisson = 0.5
    coeff = 20/3/np.pi/(1-poisson**2)
    Ex = np.linspace(min(epsilon),max(epsilon),len(epsilon))
    delta = Ex[1]-Ex[0]
    sgSigma = np.interp(Ex,epsilon,sigma)
    Ey = savgol_filter(sgSigma,window,1,deriv=1,delta=delta)
    return np.array(Ex[window:-window]),np.array(Ey[window:-window])/coeff

def ElastoStrain(epsilon,sigma,step = 100):
    poisson = 0.5
    coeff = 20/3/np.pi/(1-poisson**2)
    Ex = []
    Ey = []
    points = np.arange(0,len(epsilon),step)
    for i in range(1,len(points)):
        Ex.append( epsilon[points[i]] )        
        try:            
            coe = np.polyfit(epsilon[points[i-1]:points[i]], sigma[points[i-1]:points[i]], 1)
            Ey.append(coe[0]/coeff)
        except:
            Ey.append(0)
    return np.array(Ex),np.array(Ey)

def ElastoPressure(s,grainstep = 30,scaledistance = 500,maxindentation=9999):
    poisson = 0.5
    coeff = 20/3/np.pi/(1-poisson**2)

    E=[]

    IndexDv = [np.argmin( np.abs(s.indentation) )]    
    nextPoint = grainstep
    while(nextPoint<np.min([np.max(s.indentation),maxindentation])):
        IndexDv.append( np.argmin( np.abs(s.indentation-nextPoint) ) )
        epsilon = 0.2 * np.sqrt(s.indentation[IndexDv[-2]:IndexDv[-1]]/s.R)
        sigma = s.touch[IndexDv[-2]:IndexDv[-1]] /np.pi / s.R / s.indentation[IndexDv[-2]:IndexDv[-1]]
        try:
            coe = np.polyfit(epsilon, sigma, 1)
            E.append(coe[0]/coeff)
        except:
            E.append(0)
        nextPoint+=grainstep
    #IndexDv = np.arange(0, len(self.indentation), grainstep)
    s.IndexDv = IndexDv
    return s.indentation[IndexDv[1:]],np.array(E)

def Elastography2(s,grainstep = 30,scaledistance = 500,maxindentation=9999,mode=2):
    x = s.indentation
    y = s.touch
    yi = interp1d(x,y)
    xx = np.linspace(np.min(x)+1,np.max(x),len(x))
    yy = yi(xx)

    coeff = 3/8/np.sqrt(s.R)
    win = grainstep
    if win%2 == 0:
        win+=1
    deriv = savgol_filter(yy,win,1,delta=xx[1]-xx[0],deriv=1,mode='nearest')
    Ey = coeff*deriv/np.sqrt(xx)
    Ex = list(s.indentation)
    dwin = int((win-1)/2)
    return Ex[dwin:-dwin],Ey[dwin:-dwin]

def Elastography2withMax(s,grainstep = 30,scaledistance = 500,maxindentation=9999,mode=2):
    x = s.indentation
    y = s.touch
    if len(x)>1:
        yi = interp1d(x,y)
        max_x=np.min([np.max(s.indentation), maxindentation])
        xx = np.linspace(np.min(x)+1,max_x,int(max_x))
        yy = yi(xx)

        coeff = 3/8/np.sqrt(s.R)
        win = grainstep
        if win%2 == 0:
            win+=1
        deriv = savgol_filter(yy,win,1,delta=xx[1]-xx[0],deriv=1,mode='nearest')
        Ey = coeff*deriv/np.sqrt(xx)
        Ex = list(xx)
        dwin = int((win-1)/2)
    else:
        Ex=None
        Ey=None
    return Ex[dwin:-dwin],Ey[dwin:-dwin]

def Elastography(self,grainstep = 30,scaledistance = 500,maxindentation=9999,mode=2):
    #select one index every grainstep in nm along indentation; works with uneven step as well
    IndexDv = []  #This will contain the indexes of the slides
    nextPoint = 0
    while(nextPoint<np.min([np.max(self.indentation),maxindentation])):
        IndexDv.append( np.argmin( np.abs(self.indentation-nextPoint) ) )
        nextPoint+=grainstep
    #IndexDv = np.arange(0, len(self.indentation), grainstep)
    self.IndexDv = IndexDv
    if len(IndexDv) < 2:
        return None,None
    
    #calculate the sliced integrals
    Ex = []
    Area = []   #integrals of slices
    theta = []  #geometric coefficients

    for j in range(len(IndexDv) - 1):
        Areetta = np.trapz(self.touch[IndexDv[j]:IndexDv[j + 1]+1],self.indentation[IndexDv[j]:IndexDv[j + 1]+1]+1)
        #if Areetta >= 0:  No more need to filter out negatives 
        Area.append(Areetta)
        theta.append((j+1)**(5/2)-(j)**(5/2))
        x1 = self.indentation[IndexDv[j]]
        x2 = self.indentation[IndexDv[j+1]]            
        alpha= 0.75     #This coefficient sets whether to use the first (0), last (1) or any intermediate point for the x of the slice
        Ex.append(x1+alpha*(x2-x1))

    Area = np.array(Area)
    theta = np.array(theta)

    #Define step0 and calculate Adash and Edash for rescaling E
    step0 = np.argmin(np.abs(self.indentation[IndexDv] - scaledistance))
    Adash = np.trapz(self.touch[IndexDv[0]:IndexDv[step0]],self.indentation[IndexDv[0]:IndexDv[step0]])
    Edash = fitHertz(self,x=self.indentation[IndexDv[0]:IndexDv[step0]],y=self.touch[IndexDv[0]:IndexDv[step0]])
    if Edash is None:
        return None,None
    Omega = Edash*(step0)**(5/2)/Adash
    Ey = Omega*Area/theta #NB: Ey is in internal units

    return Ex,Ey

def gauss(x,y):
    def gaussDist(x,x0,w,A):
        return A*np.exp( -((x-x0)/w)**2 )
    if len(x)==len(y)+1:
        x = (x[1:]+x[:-1])/2.0
    popt, pcov = curve_fit(gaussDist, x,y , p0=[x[np.argmax(y)],(np.max(x)-np.min(x))/10.0,np.max(y)], maxfev=100000)
    nx = np.linspace(np.min(x),np.max(x),100)
    return popt[0],popt[1],popt[2],nx,gaussDist(nx,*popt)

def getAvWindow(x,y,xmin,xmax):
    if np.max(x) < xmax:
        return None
    imin = np.argmin( (x-xmin)**2 )
    imax = np.argmin( (x-xmax)**2 )
    return np.average(y[imin:imax])

def getAvgE(exp,xmin,xmax ):
    eall = []
    for s in exp:
        eav = getAvWindow(s.EcurveInd,s.Ecurve,xmin,xmax)
        if eav is not None:
            eall.append(eav)
    return np.average(eall)

def calcEdeep(s,index_indmin,index_indmax):
    e = []
    for i in range(index_indmin,index_indmax):
        x = s.indentation[:i]
        y = s.touch[:i]
        ecur = fitHertz(s,x,y)
        if ecur is None:
            e.append(np.nan)
        else:
            e.append(ecur*1e9)
    return e

def calculateIndentation(s):
    z = s.z-s.offsetX
    f = s.ffil-s.offsetY
    iContact = np.argmin( (z**2) )

    Yf=f[iContact:]
    # if min(Yf)<0:
    #     #Yf=Yf-min(Yf)
    #     for i, x in enumerate(Yf):
    #         if x < 0:
    #             print(x)
    #             Yf[i] = 0
    Xf=z[iContact:]
    indentation=Xf-Yf/s.k
    touch=Yf
    return indentation, touch

def filterOsc(y,pro = 0.2, winperc = 1, threshold = 25):
    # threshold is the minimum frequency to be eventually filtered
    # winperc is the width around the filtered frequency in % of the position
    # pro is the peak prominency
    #y = s.f
    #x = s.z
    ff = np.fft.rfft(y,norm=None)
    idex = find_peaks(np.log(np.abs(ff)),prominence=pro)
    xgood = np.ones(len(ff.real))>0.5
    for imax in idex[0]:
        jwin = int(imax*winperc/100)
        if imax>threshold and jwin==0:
            xgood[imax]=False
        elif imax>threshold:
            ext1 = np.max([imax-jwin,0])
            ext2 = np.min([imax+jwin+1,len(xgood)-1])
            for ii in range(ext1,ext2):
                xgood[ii]=False
    if np.sum(xgood) < 50:
        return y
    xf = np.arange(0,len(ff.real))
    yinterpreal = interp1d(xf[xgood], ff.real[xgood], kind='linear')
    yinterpimag = interp1d(xf[xgood], ff.imag[xgood], kind='linear')
    ff.real = yinterpreal(xf)
    ff.imag = yinterpimag(xf)

    return np.fft.irfft(ff,n=len(y))

def calculateNoise(segments,win=101):
    d=int((win-1)/2)
    err=[]
    for s in segments:
        remainders = s.ffil-savgol_filter(s.ffil, window_length=win, polyorder=1, deriv=0)
        err.append(np.max(remainders[d:-d]))
    return np.max(err)

def getEEE(s,win,threshold):
    if win%2==0:
        win+=1
    try:
        pdot = savgol_filter(s.ffil,polyorder=1,deriv=1,window_length=win)
    except:
        return 0,0
    return pdot/(1-pdot/s.k)
    
def eeffOffset(s,win,threshold):
    quot = getEEE(s,win,threshold)
    jj=0
    for j in range(len(quot)-1,1,-1):
        if quot[j]>threshold and quot[j-1]<threshold:
            jj=j
            break
    oX = s.z[jj]
    oY = s.ffil[jj]
    if jj>4 and jj<len(s.z)-4:
        oX = np.average(s.z[jj-4:jj+4])
        oY = np.average(s.ffil[jj-4:jj+4])    #it might be extended to use a little average of F around point jj
    return oX,oY,quot

def chiaroOffset(s,ncMin=500,ncMax=2500,offset=0,win1 = 19, win2 = 99):
    iMin = np.argmin((s.z-ncMin)**2)
    iMax = np.argmin((s.z-ncMax)**2)
    offsetY = np.average(s.ffil[iMin:iMax])
    yy = s.ffil-offsetY
    if np.max(yy)<offset or np.min(yy)>offset:
        return 0,0
    for i in range(len(yy)-win2,0,-1):
        if yy[i]>offset and yy[i-1]<offset:
            if i <= win1:
                return (s.z[i]+s.z[i-1])/2.0,offsetY
            else:
                polx = s.z[i-win1:i+win2]
                poly = yy[i-win1:i+win2]
                pol = np.poly1d(np.polyfit(polx, poly, 4))
                if offset == 0:
                    return polx[np.argmin((pol(polx))**2)],offsetY
                else:
                    for toR in range(win2,len(s.z),win2):
                        newx = s.z[i:i+toR]
                        newy = pol(newx)
                        if np.max(newy)>0:
                            break
                    for toL in range(win1,i,win1):
                        newx = s.z[i-toL:i]
                        newy = pol(newx)
                        if np.min(newy)<0:
                            break
                    newx = s.z[i-toL:i+toR]
                    newy = pol(newx)
                    return newx[np.argmin( newy**2 )],offsetY
    return 0,0

def NanosurfOffset(s, step=50, length=500, threshold_exp = 0.1, threshold_len_straight = 0, thresholdfactor_mean_exp_before_CP=0.5, threshold_invalid=10):
    z = s.z
    f = s.ffil
    s.threshold_exp=threshold_exp

    min_f = min(f)
    f_nonzero = [i - min_f + 1 for i in f]
    min_z = min(z)
    z_nonzero = [i - min_z + 1 for i in z]
    log_z = np.log(z_nonzero)
    log_f = np.log(f_nonzero)

    exponents = []
    exps_norm = []
    over_threshold = []
    first_over_threshold=[]
    len_straight = 0
    m=0

    for i in range(len(f) - length, 0, -step):
        part = log_f[i:i + length]
        z_part = log_z[i:i + length]
        exponent = np.polyfit(z_part, part, 1)[0]
        if i == len(f) - length:
            exp_max = exponent
        if exponent > exp_max:
            exp_max = exponent
        exp_norm = exponent / exp_max
        for j in range(0, step):
            exponents.append(exponent)
            exps_norm.append(exp_norm)
        if exp_norm > threshold_exp:
            over_threshold.append(i)
            m=m+1
            if m>1:
                if over_threshold[-2]-over_threshold[-1]>step:
                    first_over_threshold.append(over_threshold[-2])
        if abs(exp_norm) < threshold_exp:
            len_straight = len_straight + 1
    first_over_threshold.append(over_threshold[-1])
    exponents.reverse()
    exps_norm.reverse()
    over_threshold.reverse()
    z_exps = z[:len(exponents)]

    imax_exp = 0
    if len(first_over_threshold) >= 1:
        imax_exp = first_over_threshold[0]
    s.imax_exp=imax_exp

    bol = True
    mean_before_CP= np.mean(exps_norm[:imax_exp])
    if mean_before_CP >thresholdfactor_mean_exp_before_CP*threshold_exp:
        bol = False
    if len_straight*step < threshold_len_straight:
        bol = False
    if imax_exp == 0:
        bol = False

    offsetX=s.z[imax_exp]
    offsetY=s.ffil[imax_exp]
    return bol,offsetX,offsetY, z_exps, exps_norm


def NanosurfOffsetDeriv(s, win=1000, step_z=50, factor=5, threshold_slopes=0.2, threshold_len_straight=1000, threshold_invalid=10):
    ymax=[]
    xz0=[]
    z=s.z-min(s.z)
    P = s.f - min(s.f) + 10
    coeff = 3 / 8 / np.sqrt(s.R)
    if win % 2 == 0:
        win += 1
    pdot = savgol_filter(P, win, 1, delta=z[1] - z[0], deriv=1, mode="interp")
    blob = pdot / (1 - pdot / s.k)

    z0s=np.linspace(int(min(z)), int(max(z)-step_z), int((max(z)-min(z))/step_z))
    for z0_i in z0s:
        down = np.sqrt(abs(z - z0_i - P / s.k))
        E= coeff * blob / down
        ind, i0 = IndentationForDerivative(s, z0_i)
        y= E[i0:] * 1e9
        if len(y)<10:
            bol=False
            pass
        else:
            xz0.append(z0_i)
            ymax.append(np.median(y[5:25]))

    x_slopes=[]
    slopes=[]
    for i,x in enumerate(z0s[:-(factor+1)]):
        x=int(x)
        x_part=z0s[i:(i+factor)]
        y_part=ymax[i:(i+factor)]
        slope=np.polyfit(x_part, y_part, 1)[0]
        slopes.append(slope)
        x_slopes.append(x)

    min_slopes=min(slopes)
    max_slopes=max(slopes)
    slopes_norm=[(x-min_slopes)/(max_slopes-min_slopes) for x in slopes]
    s.threshold_slopes=threshold_slopes
    above_threshold=[]
    firsts=[]
    m=0
    for i,x in enumerate(reversed(slopes_norm)):
        if x > threshold_slopes:
            above_threshold.append(i)
            m=m+1
            if m>2:
                if i-above_threshold[-2]>1:
                    firsts.append(above_threshold[-2])
    if len(firsts)<1:
        bol=False
        ind_z0s=0
    else:
        ind_z0s=firsts[0]
    z0_CP=x_slopes[ind_z0s]
    ind_CP=np.argmin(np.abs(s.z-z0_CP))

    bol = True
    if ind_CP < threshold_len_straight:
        bol = False
    if ind_CP == 0:
        bol = False

    offsetX=s.z[ind_CP]
    offsetY=s.f[ind_CP]

    return bol, offsetX, offsetY, xz0, ymax, x_slopes, slopes_norm

def P_derivative(s, z0=0, win=20, savgol_mode='interp'):
    z = s.z-min(s.z)
    P = s.f-min(s.f)+10
    coeff = 3 / 8 / np.sqrt(s.R)
    down = np.sqrt(abs(z - z0 - P / s.k))
    if win % 2 == 0:
        win += 1
    pdot = savgol_filter(P, win, 1, delta=z[1] - z[0], deriv=1, mode=savgol_mode)
    blob = pdot / (1 - pdot / s.k)
    return coeff * blob / down

def IndentationForDerivative(s, z0=0):
    z=s.z-min(s.z)
    i0 = np.argmin((z - z0) ** 2)
    ind = z[i0:] - z0 - s.f[i0:] / s.k
    return ind, i0

def Nanosurf_FindInvalidCurves(s, threshold_invalid=10):
    s.bol2=None
    ind=np.argmin(abs(s.z-s.offsetX))
    if ind<199:
        s.bol2 = False
    else:
        f_abs = np.absolute(s.ffil[200:ind])
        val=max(f_abs)
        f_abs2=np.absolute(s.ffil[-1000:-100])
        val2=max(f_abs2)
        if val>threshold_invalid or val2<0.5*threshold_invalid:
            s.bol2=False
        else:
            s.bol2=True
    return s.bol2

def getHertz(E,R,threshold,indentation=True):
    poisson = 0.5
    if indentation is True:
        x = np.linspace(0,threshold,200)
    else:
        xmax = (((3.0/4.0) * ((1 - poisson ** 2)/E)  * threshold)**2/R ) **(1/3)
        x = np.linspace(0,xmax,200)

    return x,(4.0 / 3.0) * (E / (1 - poisson ** 2)) * np.sqrt(R * x ** 3)

def fitHertz(s,x=None,y=None):
    if x is None:
        x = s.indentation[:s.indMax]
        y = s.touch[:s.indMax]
    seeds = [1000.0/1e9]
    #NB the curve is forced to have F=0 at indentation 0
    try:
        R = s.R
        def Hertz(x,E):
            x = np.abs(x)
            poisson = 0.5
            # Eeff = E*1.0e9 #to convert E in GPa to keep consistency with the units nm and nN
            return (4.0 / 3.0) * (E / (1 - poisson ** 2)) * np.sqrt(R * x ** 3)

        popt, pcov = curve_fit(Hertz, x,y , p0=seeds, maxfev=10000)
        Einternal = popt[0]
        return Einternal
    except (RuntimeError,ValueError):
        return None

def noisify(y,intensity=1.0):
    random.seed()
    for i in range(len(y)):
        y[i]=y[i]+2*(random.random()-0.5)*intensity
    return y

def standardHertz(x,E,R,poisson=0.5):
    return (4.0 / 3.0) * (E / (1 - poisson ** 2)) * np.sqrt(R * x ** 3)

def LayerStd(x,E0,Eb,d0,R,poisson=0.5):
    x[x<0]=0
    a = np.sqrt(R*x)
    E = Eb+(E0-Eb)*np.exp(-a/d0)
    return 4.0*E*a**3/R/3.0/(1-poisson**2)

def LayerRoss(x,E1,E2,h,R,poisson=0.5):
    x[x<0]=0
    a = np.sqrt(R*x)
    sopra = 0.85*(a/h)+3.36*(a/h)**2
    expo = 0.72-0.34*(a/h)+0.51*(a/h)**2
    coe = (sopra+1)/(sopra*(E1/E2)**expo+1)
    F = 4.0*E1*coe*a**3/3.0/R/(1-poisson**2)
    return F

def ExpDecay(x,E0,Eb,d0,R):
    x[x<0]=0
    a=np.sqrt(R*x)
    return Eb+(E0-Eb)*np.exp(-a/d0)

def fitExpDecay(x,y,R):
    seeds=[5000/1e9,1000/1e9,200]
    try:
        def TheExp(x,E0,Eb,d0):
            x[x<0]=0
            a=np.sqrt(R*x)
            return Eb+(E0-Eb)*np.exp(-a/d0)
        popt, pcov = curve_fit(TheExp, x,y , p0=seeds, maxfev=10000)
        return popt
    except (RuntimeError,ValueError):

        return None