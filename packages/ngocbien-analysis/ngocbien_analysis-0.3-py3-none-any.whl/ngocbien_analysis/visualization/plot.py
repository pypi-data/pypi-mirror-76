import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime
import seaborn as sns
import os
COLOR = [(0.3, 0.9, 0.4, 0.6), (0.3, 0.1,0.4,0.6)]


class DistributionPlot:
    def __init__(self, data1, data2=None, is_save=True,  **kwargs):
        self.data1 = data1
        self.data2 = data2
        self.nmax = 9
        self.label = ['data1', 'data2']
        self.num_types = ['float32', 'float64', 'int16', 'int32', 'int64', 'bool', 'int8']
        self.is_save = is_save
        self.alpha = [.6, .4]
        self.width = .9
        self.wspace = .15
        self.hspace = .25
        self.disable_xticks = False
        self.disable_yticks = True
        if self.is_save:
            self.get_or_create_dir()

    def get_figure_size(self, n):

        if n<=3:
            return (12,5)
        elif n<=6:
            return (14,6)
        elif n<=9:
            return (17,8)
        else:
            return (17,10)
    
    def get_ax(self, n):

        if n<1:
            return None
        if n<=3:
            return (1,n)
        elif n==4:
            return (2,2)
        elif n<=6:
            return (2,3)
        elif n<=9:
            return (3,3)
        else:
            row = int(np.sqrt(n))
            col = n//row
            while row*col<n:
                col+=1
            return (row, col)

    def get_or_create_dir(self):

        dir = os.getcwd()
        sub_dir = "\\%s_%s\\picture\\"%(self.label[0], self.label[1])
        self.dir = dir+sub_dir
        if not os.path.isdir(self.dir):
            os.makedirs(self.dir)
        return self

    def file_name(self, suffix, prefix=None):
        import datetime
        t = datetime.datetime.now()
        t = str(t).split('.')[0] # bỏ đi phần mili seconds
        t = ' '.join(t.split(':'))
        if prefix is not None:
            return self.dir+"%s %s %s.png"%(prefix, t, suffix)
        else:
            return self.dir+"%s %s.png"%(t, suffix)

    def __plot_dist__(self, name, ax):
        try:
            sns.kdeplot(self.data1[name], shade=True, color=COLOR[0], label=self.label[0], alpha=self.alpha[0], ax=ax)
            sns.kdeplot(self.data2[name], shade=True, color=COLOR[1], label=self.label[1], alpha=self.alpha[1], ax=ax)
        except:
            #print('%s field can not estimated by kde'%name)
            ax.hist(self.data1[name], bins=100, alpha=self.alpha[0], label=self.label[0], color=COLOR[0], density=True)
            ax.hist(self.data2[name], bins=100, alpha=self.alpha[1], label=self.label[1], color=COLOR[1], density=True)
        ax.title.set_text(name)
        if self.disable_yticks:
            ax.set_yticks([])
        if self.disable_xticks:
            ax.set_xticks([])

    def plot_dist(self, cols):

        size = self.get_figure_size(len(cols))
        ax_ = self.get_ax(len(cols))
        if ax_ is None:
            return None
        fig, ax = plt.subplots(ncols=ax_[1], nrows=ax_[0])
        #plt.tick_params(axis='both', which='both')
        #plt.axis('off')
        fig.set_figheight(size[1])
        fig.set_figwidth(size[0])
        plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=self.wspace, hspace=self.hspace)
        index = 0
        if ax_[0] == 1 and ax_[1] == 1:
            name = cols[index]
            self.__plot_dist__(name, ax)
        elif ax_[0] == 1 or ax_[1] == 1:
            for row in ax:
                if index>=len(cols):
                    continue
                name = cols[index]
                self.__plot_dist__(name, row)
                index += 1
        else:
            for col in ax:
                for row in col:
                    if index >= len(cols):
                        continue
                    else:
                        name = cols[index]
                        index += 1
                        self.__plot_dist__(name, row)
        if self.is_save:
            path = self.file_name(suffix='')
            plt.savefig(path, bbox_inches='tight', dpi=1200)
        plt.suptitle('comparison of distributions between %s and %s'%(self.label[0], self.label[1]), fontsize=16, color='green')
        plt.show()

    def __bar__(self, col, ax):
        def index_rot(index):
            rot = 45
            use_index = True
            max_lenght = max([len(str(i)) for i in index])
            if max_lenght>10 or len(index)>10:
                use_index = False
            if max_lenght <= 4:
                rot = 0
            elif max_lenght<10 and len(index)<10:
                rot = 0
            return rot, use_index
        index = set(set(self.data1[col].unique()) | set(self.data2[col].unique()))
        index = list(index)
        if len(index) > 100:
            index = self.data1[col].value_counts().head(100).index
        dfx = pd.DataFrame(index=index)
        try:
            dfx[self.label[0]] = self.data1[col].value_counts(dropna=False)/len(self.data1)*100
            dfx[self.label[1]] = self.data2[col].value_counts(dropna=False)/len(self.data2)*100
        except IndexError:
            dfx[self.label[0]] = self.data1[col].value_counts(dropna=False).iloc[:len(index)]/len(self.data1)*100
            x = self.data2[col].value_counts(dropna=False)/len(self.data2)*100
            dfx[self.label[1]] = x.loc[x.index.intersection(index)]
        dfx = dfx.fillna(0)
        rot, use_index = index_rot(index)
        if use_index:
            xticks = index
        else:
            xticks = []
        #xticks = []
        yticks = [10, 20, 40, 80, 100]
        if len(xticks) == 0:
            dfx.plot.bar(rot=rot, ax=ax, color=COLOR, title=col,  width=self.width, xticks=xticks, yticks=yticks)
        else:
            dfx.plot.bar(rot=rot, ax=ax, color=COLOR, title=col,  width=self.width, yticks=yticks)
        if self.disable_yticks:
            ax.set_yticks([])
        if self.disable_xticks:
            ax.set_xticks([])


    def plot_bar(self, cols):

        size = self.get_figure_size(len(cols))
        ax_ = self.get_ax(len(cols))
        if ax_ is None:
            return None
        fig, ax = plt.subplots(ncols=ax_[1], nrows=ax_[0])
        fig.set_figheight(size[1])
        fig.set_figwidth(size[0])
        plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=self.wspace, hspace=self.hspace)
        index = 0
        if ax_[0] == 1 and ax_[1] == 1:
            name = cols[index]
            self.__bar__(name, ax)
        elif ax_[0] == 1 or ax_[1] == 1:
            for row in ax:
                if index >= len(cols):
                    continue
                else:
                    name = cols[index]
                    index += 1
                self.__bar__(name, row)
        else:
            for col in ax:
                for row in col:
                    if index >= len(cols):
                        continue
                    else:
                        name = cols[index]
                        index += 1
                    self.__bar__(name, row)
        plt.suptitle('comparison of distributions between %s and %s'%(self.label[0], self.label[1]), fontsize=16, color='green')
        if self.is_save:
            path = self.file_name(suffix='')
            plt.savefig(path, bbox_inches='tight', dpi=1200)
        plt.show()

    def plot2data(self):

        import random
        assert set(self.data1.columns) == set(self.data2.columns)
        num = [col for col in self.data1.columns if self.data1[col].dtypes in self.num_types]
        object = [col for col in self.data1.columns if self.data1[col].dtypes == 'object']
        if len(num)>0:
            self.data1[num] = self.data1[num].astype('float32')
            self.data2[num] = self.data2[num].astype('float32')
            stop = 0
            step = len(num)//self.nmax if len(num)%self.nmax==0 else len(num)//self.nmax+1
            # nếu len(num) không chia hết cho 9 thì cần add thêm 1:
            for i in range(step):
                start = stop
                stop = start+self.nmax
                stop = min(stop, len(object)-1)
                cols = num[start:stop]
                self.plot_dist(cols)
        if len(object) > 0:
            stop = 0
            step = len(object)//self.nmax if len(object)%self.nmax==0 else len(object)//self.nmax+1
            # nếu len(object) không chia hết cho 9 thì cần add thêm 1
            for i in range(step):
                start = stop
                stop = start+self.nmax
                stop = min(stop, len(object)-1)
                cols = object[start:stop]
                self.plot_bar(cols)
