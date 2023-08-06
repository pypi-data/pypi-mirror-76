import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from .config import *


def print_time(seconds):

    hours=int(seconds//(60*60))
    minutes=int((seconds-hours*60*60)//60)
    seconds=int(seconds-minutes*60-hours*60*60)
    if hours>0:
        return "%s hours %s mins %s secs"%(hours,minutes,seconds)
    elif minutes>0:
        return "%s mins, %s secs"%(minutes,seconds)
    else:
        return "%s secs"%seconds


def memory_usage():

    import sys
    # These are the usual ipython objects, including this one you are creating
    x=10**9
    ipython_vars=['In','Out','exit','quit','get_ipython','ipython_vars']
    # Get a sorted list of the objects and their sizes
    return sorted([(x,sys.getsizeof(globals().get(x))) for x in dir() if\
                   not x.startswith('_') and x not in sys.modules and x not in ipython_vars],\
                  key=lambda x:x[1],reverse=True)


def extract_package_from_notebook():

    import os
    this_path=os.getcwd()
    if 'notebook' in this_path:
        this_path=this_path.split('\\')[:-1]
        this_path='\\'.join(this_path)
    os.chdir(this_path)
    print('current path now is:')
    print(os.getcwd())



def up_sample(df, target=None):
    from sklearn.utils import resample
    if target is not None:
        df['target'] = target
    df_0=df[df.target==0]
    df_1=df[df.target==1]
    # upsample minority
    if len(df_1)<len(df_0):
        df_1=resample(df_1,
                      replace=True,  # sample with replacement
                      n_samples=len(df_0),  # match number in majority class
                      random_state=49)  # reproducible results
    else:
        df_0=resample(df_0,replace=True,  # sample with replacement
                      n_samples=len(df_1),  # match number in majority class
                      random_state=49)  # reproducible results
    df=pd.concat([df_0,df_1])
    target = df.target
    df = df.drop(columns=['target']).astype('float32')
    return df, target


def pick_color(n=1):
    import random
    colors=["blue","black","brown","red","yellow","green","orange","beige","turquoise","pink"]
    random.shuffle(colors)
    if n==1:
        return colors[0]
    else:
        colors_=[]
        for i in range(n):
            colors_.append(random.choice(colors))
        return colors_


def get_path(how='picture', key='data_V2_1'):

    from datetime import datetime
    now = datetime.now()
    current_time = now.strftime("%d %m %y %H %M")  # will add this time to the name of file distinct them
    from config import model_path
    path = picture_path + current_time
    if how=='picture':
        path += key + '.png'
    else:
        print('error key!')
    return path
