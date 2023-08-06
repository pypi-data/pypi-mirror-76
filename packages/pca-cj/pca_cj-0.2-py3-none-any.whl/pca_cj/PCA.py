# -*- coding: utf-8 -*-
"""
Created on Sun Aug 16 17:15:51 2020

@author: cj
"""
import numpy as np
def PCA(X,cor=True,cov_scaling=True,center=True):
    mean=np.apply_along_axis(np.mean,0,X)
    std=np.apply_along_axis(np.std,0,X)
    if center:
        X=X- mean
    if np.isnan(X).sum()!=0:
        ValueError
    else:
        if cor:
            mat=np.corrcoef(X.T)
        elif cov_scaling:
            def standardization(x):
                std=np.apply_along_axis(np.std,0,X)
                mean=np.apply_along_axis(np.mean,0,X)
                z=(X-mean)/std
                return [z,mean,std]

            def inv_standardization(z,mean,sd):
                x=z*std+mean
                return x
            
            z,mean,std=standardization(X)
            mat=np.cov(z.T)
#            inv_standardization(z,mean,std)
        else:
            mat=np.cov(X.T)

    u,s,v = np.linalg.svd(mat.T)
    eig_pairs=[(np.abs(s[i]),v.T[:,i]) for i in range(len(s))]
    eig_pairs.sort()
    eig_pairs.reverse()
    matrix_w =np.hstack([i[1].reshape(X.shape[1],1) for i in eig_pairs]) 
    Y = X.dot(matrix_w)
    matrix_w.shape
    X.shape
    return [Y,mean,std,matrix_w]
#from sklearn.datasets import load_iris
#import pandas as pd
#df= load_iris()
#
#df=pd.concat([pd.DataFrame(df.data),pd.Series(df.target)],axis=1)
#df.columns=['sepal_len', 'sepal_wid', 'petal_len', 'petal_wid', 'class']
#
#df.tail()
#X = df.iloc[:,0:4].values
#y = df.iloc[:,4].values
#
#finelDF,mean,std,matrix_w=PCA(X,cor=False,cov_scaling=False)
#finelDF,mean,std,matrix_w=PCA(X,cor=True)
#
#
#from matplotlib import pyplot as plt
#
#fig = plt.figure(figsize = (8,8))
#ax = fig.add_subplot(1,1,1) 
#ax.set_xlabel('Principal Component 1', fontsize = 15)
#ax.set_ylabel('Principal Component 2', fontsize = 15)
#ax.set_title('2 component PCA', fontsize = 20)
#targets = [2, 1, 0]
#colors = ['r', 'g', 'b']
#for target, color in zip(targets,colors):
#    indicesToKeep = y== target
#    ax.scatter(finelDF[indicesToKeep ,0]
#               , finelDF[indicesToKeep ,1]
#               , c = color
#               , s = 50)
#ax.legend(targets)
#ax.grid()
#
#a=PCA(X[1:50],cor=False,cov_scaling=False)
##prediction
#pred=(X[51:,:]-a[1]).dot(a[3])



