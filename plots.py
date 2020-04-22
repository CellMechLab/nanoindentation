import csv
import numpy as np
import math
import matplotlib.pyplot as plt

class indentAll():
    pass
class indentMed():
    pass
class elastoAll():
    pass
class elastoMed():
    pass
class histo():
    pass
class elastoHisto():
    pass
class bar():
    pass

class plots():
    def __init__(self, parent=None):
        self.workingdir = './'
        self.indentAll = indentAll
        self.indentMed = indentMed
        self.elastoAll = elastoAll
        self.elastoMed = elastoMed
        self.histo = histo
        self.elastoHisto = elastoHisto
        self.bar = bar

    def LoadData(self, fnames):
        objects=[self.indentAll, self.indentMed, self.elastoAll, self.elastoMed, self.histo, self.elastoHisto]
        for i, o in enumerate(objects):
            if fnames[i] is not None:
                with open(fnames[i], newline='') as csvfile:
                    reader=csv.reader(csvfile, delimiter=',')
                    labels=[]
                    data=[]
                    for row in reader:
                        label=row[0]
                        row=np.asarray(row[1:])
                        row=row.astype(float)
                        labels.append(label)
                        data.append(row)
                o.labels=labels
                o.data=data

    def LoadData_Conditions(self, fnames):
        self.elastoMed.datas=[]
        for i in range(len(fnames)):
            with open(fnames[i], newline='') as csvfile:
                reader=csv.reader(csvfile, delimiter=',')
                labels=[]
                data=[]
                for row in reader:
                    label=row[0]
                    row=np.asarray(row[1:])
                    row=row.astype(float)
                    labels.append(label)
                    data.append(row)
            self.elastoMed.labels=labels
            self.elastoMed.datas.append(data)

    def LoadData_BarPlots(self, fname):
        with open(fname, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            conds=[]
            labels = []
            data = []
            for i, row in enumerate(reader):
                if i==0:
                    self.bar.mags = row[2:]
                else:
                    cond = row[0]
                    label = row[1]
                    row = np.asarray(row[2:])
                    row = row.astype(float)
                    conds.append(cond)
                    labels.append(label)
                    data.append(row)
            self.bar.conds=conds
            self.bar.labels=labels
            self.bar.data=data

    def LoadData_BarPlots_SingleValues(self, fname):
        with open(fname, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            pos=[]
            val=[]
            std=[]
            for i, row in enumerate(reader):
                if i>=2:
                    row = np.asarray(row[1:])
                    row = row.astype(float)
                    if (i-2)%3==0:
                        pos.append(row)
                    if (i-2-1)%3==0:
                        val.append(row)
                    if (i-2-2)%3==0:
                        std.append(row)
            self.bar.scatterx = pos
            self.bar.scattery = val
            self.bar.scatterstd = std

    def InitiateFigure(self, figstr, figsize):
        fig, axs = plt.subplots(figstr[0], figstr[1], figsize=figsize)
        self.figure=fig
        self.axes=axs
        self.lenax_x = figstr[0]
        self.lenax_y = figstr[1]

    def FindPosition(self, pos):
        if self.lenax_x==1:
            ax = self.axes[int(pos)]
        else:
            pos1=int(math.floor(pos/self.lenax_y))
            pos2=int(pos-pos1*self.lenax_y)
            ax = self.axes[pos1][pos2]
        return ax

    def AdjustAxis_ylim(self, ax, x, y):
        lims = ax.get_xlim()
        i = np.where((x > lims[0]) & (x < lims[1]))[0]
        ax.set_ylim(y[i].min(), y[i].max()*1.1)

    def ForceCurves(self, pos=1, ax_lim=None):
        ax=self.FindPosition(pos)
        Forces=self.indentAll.data[2:]
        HertzFit=self.indentMed.data[0:2]
        maxForceAtXlim = 0
        for i in range(0, len(Forces), 2):
            ax.plot(Forces[i], Forces[i+1], color='black', linewidth=0.1)
            if ax_lim is not None and len(Forces[i+1])>ax_lim[0]:
                if Forces[i+1][ax_lim[0]]>maxForceAtXlim:
                    maxForceAtXlim = Forces[i+1][ax_lim[0]]
                    indMaxCurve = i
        ax.plot(HertzFit[0], HertzFit[1], color='lime', linewidth=2)
        ax.set_xlabel('\u03B4 (nm)')
        ax.set_ylabel('F (nN)')
        if ax_lim is not None:
            ax.set_xlim(0,ax_lim[0])
            if len(ax_lim)>1:
                ax.set_ylim(ax_lim[1], ax_lim[2])
            else:
                self.AdjustAxis_ylim(ax, Forces[indMaxCurve], Forces[indMaxCurve+1])

    def ForceCurvesWithAverage(self, pos=1, ax_lim=None):
        ax=self.FindPosition(pos)
        Forces=self.indentAll.data[2:]
        MedCurve=self.indentMed.data[0:2]
        MedErr = self.indentMed.data[3:5]
        Fit= self.indentMed.data[5:7]
        maxForceAtXlim = 0
        for i in range(0, len(Forces), 2):
            ax.plot(Forces[i], Forces[i+1], color='black', linewidth=0.1)
            if ax_lim is not None and len(Forces[i+1])>ax_lim[0]:
                if Forces[i+1][ax_lim[0]]>maxForceAtXlim:
                    maxForceAtXlim = Forces[i+1][ax_lim[0]]
                    indMaxCurve = i
        ax.plot(MedCurve[0], MedCurve[1], color='blue', linewidth=1)
        ax.fill_between(MedCurve[0], MedErr[0], MedErr[1], color='red', alpha=0.5)
        ax.plot(Fit[0], Fit[1], color='lime', linewidth=2)
        ax.set_xlabel('\u03B4 (nm)')
        ax.set_ylabel('F (nN)')
        if ax_lim is not None:
            ax.set_xlim(0,ax_lim[0])
            if len(ax_lim)>1:
                ax.set_ylim(ax_lim[1], ax_lim[2])
            else:
                self.AdjustAxis_ylim(ax, Forces[indMaxCurve], Forces[indMaxCurve+1])

    def ElastoAll(self, mode=None, pos=2, ax_lim=None):
        ax=self.FindPosition(pos)
        AllData=self.elastoAll.data
        MedCurve=self.elastoMed.data[0:2]
        MedErr = self.elastoMed.data[3:5]
        Fit= self.elastoMed.data[5:]
        for i in range(0, len(AllData), 2):
            ax.plot(AllData[i], AllData[i+1], color='black', linewidth=0.1, alpha=0.25)
        ax.plot(MedCurve[0], MedCurve[1], color='blue', linewidth=1)
        ax.fill_between(MedCurve[0], MedErr[0], MedErr[1], color='red', alpha=0.5)
        ax.plot(Fit[0], Fit[1], color='lime', linewidth=2)
        ax.set_xlabel('\u03B4 (nm)')
        ax.set_ylabel('E (Pa)')
        if ax_lim is not None:
            ax.set_xlim(0,ax_lim[0])
            if len(ax_lim)>1:
                ax.set_ylim(ax_lim[1], ax_lim[2])

    def ElastoMed_Conditions(self, mode=None, pos=1):
        ax=self.FindPosition(pos)
        colors=['blue', 'red', 'black', 'lime', 'yellow', 'cyan', 'magenta']
        for i in range(len(self.elastoMed.datas)):
            MedCurve=self.elastoMed.datas[i][0:2]
            MedErr = self.elastoMed.datas[i][3:5]
            Fit= self.elastoMed.datas[i][5:]
            ax.plot(MedCurve[0], MedCurve[1], color=colors[i], linewidth=1)
            # ax.fill_between(MedCurve[0], MedErr[0], MedErr[1], color=colors[i], alpha=0.1)
            # ax.plot(Fit[0], Fit[1], color=colors[i], linewidth=2)
            # if mode=='bilayer':
            #     ax.plot(Fit[2], Fit[3], color=colors[i], linewidth=2)
        ax.set_xlim(0,1000)
        ax.set_ylim(0, 12000)
        ax.set_xlabel('\u03B4 (nm)')
        ax.set_ylabel('E (Pa)')

    def ElastoNoAverage(self, mode=None, pos=2, ax_lim=None):
        ax=self.FindPosition(pos)
        AllData=self.elastoAll.data
        print(AllData[1])
        Fit= self.elastoMed.data[5:]
        for i in range(0, len(AllData), 2):
            ax.plot(AllData[i], AllData[i+1], color='black', linewidth=0.1, alpha=0.25)
            print(i,AllData[i],AllData[i+1])
        ax.plot(Fit[0], Fit[1], color='lime', linewidth=2)
        ax.set_xlabel('\u03B4 (nm)')
        ax.set_ylabel('E (Pa)')
        if ax_lim is not None:
            ax.set_xlim(0,ax_lim[0])
            if len(ax_lim)>1:
                ax.set_ylim(ax_lim[1], ax_lim[2])
        from matplotlib.ticker import ScalarFormatter
        ax.get_yaxis().get_major_formatter().set_useOffset(False)

    def Histo(self, mode=None, pos=3):
        ax=self.FindPosition(pos)
        FromHertz=self.histo.data[:7]
        FromElasto=self.histo.data[7:]
        ax.hist(FromHertz[2], bins='auto', density=True, color='lime', alpha=0.5)
        ax.plot(FromHertz[5], FromHertz[6], color='lime')
        if mode=='single':
            #ax = ax.twinx()
            ax.hist(FromElasto[2], bins='auto', density=True, color='red', alpha=0.5)
            ax.plot(FromElasto[5], FromElasto[6], color='red')
        ax.set_xlabel('E (Pa)')
        ax.set_ylabel('frequency')

    def BarPlotsInsteadOfHisto(self, pos=3):
        ax = self.FindPosition(pos)
        FromHertz=self.indentMed.data[7:9]
        FromElasto=self.elastoMed.data[7:9]
        print(FromHertz)
        print([FromHertz[0], FromElasto[0]])
        ax.bar(x=[0,1], height=[FromHertz[0][0], FromElasto[0][0]], tick_label=['Hertz', 'Elasto'], yerr=[FromHertz[1][0], FromElasto[1][0]], color=['lime', 'red'], alpha=0.5)

    def BarPlots(self,pos):
        num_conds=int(len(self.bar.conds)/3)
        for i in range(len(self.bar.mags)):
            ax = self.FindPosition(pos+i)
            conds=[]
            means=[]
            stds=[]
            sigs=[]
            colors=[]
            for n in range(0, num_conds*3, 3):
                conds.append(self.bar.conds[n])
                means.append(self.bar.data[n][i])
                stds.append(self.bar.data[n+1][i])
                sigs.append(self.bar.data[n+2][i])
                if self.bar.data[n + 2][i]==0:
                    colors.append('blue')
                else:
                    colors.append('red')
            ax.bar(range(num_conds), means, tick_label=conds, yerr=stds, color=colors)
            ax.set_title(self.bar.mags[i])
            ax.set_xticklabels(labels= conds, rotation=45)
            if i<3:
                ax.set_ylabel('E (Pa)')
            else:
                ax.set_ylabel('d (nm)')
        plt.tight_layout()

    def BarPlots_WithSingleMeasurements(self,pos):
        num_conds=int(len(self.bar.conds)/3)
        for i in range(len(self.bar.mags)):
            ax = self.FindPosition(pos+i)
            conds=[]
            means=[]
            stds=[]
            sigs=[]
            colors=[]
            for n in range(0, num_conds*3, 3):
                conds.append(self.bar.conds[n])
                means.append(self.bar.data[n][i])
                stds.append(self.bar.data[n+1][i])
                sigs.append(self.bar.data[n+2][i])
                if self.bar.data[n + 2][i]==0:
                    colors.append('blue')
                else:
                    colors.append('red')
            ax.bar(range(num_conds), means, tick_label=conds, yerr=stds, color=colors)
            ax.plot(self.bar.scatterx[i], self.bar.scattery[i], 'o', color='black')
            ax.set_title(self.bar.mags[i])
            ax.set_xticklabels(labels= conds, rotation=45)
            if i<3:
                ax.set_ylabel('E (Pa)')
            else:
                ax.set_ylabel('d (nm)')
        plt.tight_layout()

    def ElastoHisto(self, pos=0):
        E0_data=self.elastoHisto.data[:7]
        Eb_data=self.elastoHisto.data[7:14]
        d0_data = self.elastoHisto.data[14:]
        data=[E0_data, Eb_data, d0_data]
        for i in range(3):
            dat=data[i]
            ax = self.FindPosition(pos+i)
            ax.hist(dat[2], bins='auto', density=True, color='lime', alpha=0.5)
            ax.plot(dat[5], dat[6], color='lime')
            if i<3:
                ax.set_xlabel('E (Pa)')
            else:
                ax.set_xlabel('d (nm)')
            ax.set_ylabel('frequency')

    def gauss(x, y):
        def gaussDist(x, x0, w, A):
            return A * np.exp(-((x - x0) / w) ** 2)

        if len(x) == len(y) + 1:
            x = (x[1:] + x[:-1]) / 2.0
        popt, pcov = curve_fit(gaussDist, x, y, p0=[x[np.argmax(y)], (np.max(x) - np.min(x)) / 10.0, np.max(y)],
                               maxfev=100000)
        nx = np.linspace(np.min(x), np.max(x), 100)
        return popt[0], popt[1], popt[2], nx, gaussDist(nx, *popt)

    def SaveFigSvg(self, fname):
        plt.savefig(fname+'.svg')

    def SaveFigPng(self, fname):
        plt.savefig(fname+'.png')