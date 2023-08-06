# -*- coding: utf-8 -*-
"""
Created on Sun Aug 16 21:16:37 2020

@author: cj
"""


def kernel_PCA(X,gamma,n_components,scaling=True):
    if scaling:
        def standardization(x):
                    std=np.apply_along_axis(np.std,0,X)
                    mean=np.apply_along_axis(np.mean,0,X)
                    z=(X-mean)/std
                    return [z,mean,std]
        X,mean,std=standardization(X)
    dist_sq = np.sum((X[:, np.newaxis, :] - X[np.newaxis, :, :]) ** 2, axis = -1)
    K = exp(-gamma * dist_sq)
    N = K.shape[0]
    one_n = np.ones((N, N)) / N
    K = K - one_n.dot(K) - K.dot(one_n) + one_n.dot(K).dot(one_n)
    s,v = np.linalg.eigh(K)
    eig_pairs=[(np.abs(s[i]),v[:,i]) for i in range(len(s))]
    eig_pairs.sort()
    eig_pairs.reverse()
    Y= np.column_stack([eig_pairs[i][1] for i in range(n_components)])
    lambdas= np.column_stack([eig_pairs[i][0] for i in range(n_components)])
    
    return Y,lambdas
#
#X, y = make_moons(n_samples=100, random_state=123)
#X_skernpca ,lambdas= kernel_PCA(X,n_components=2, gamma=15,scaling=False)
#
#plt.scatter(X_skernpca[y == 0, 0], X_skernpca[y == 0, 1],
#            color='red', marker='^', alpha=0.5)
#plt.scatter(X_skernpca[y == 1, 0], X_skernpca[y == 1, 1],
#            color='blue', marker='o', alpha=0.5)
#
#plt.xlabel('PC1')
#plt.ylabel('PC2')
#plt.tight_layout()
#plt.show()